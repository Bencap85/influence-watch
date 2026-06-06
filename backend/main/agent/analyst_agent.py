import json
import uuid
import re
import logging
from typing import Dict, Any
from main.agent.mcp_http_client import MCPHttpClient
from main.processing.openai_http import post
from main.agent.prompt import INTEL_ANALYST_SYSTEM_PROMPT
from main.agent.tool_definitions import TOOLS


class AnalystAgent:
    def __init__(self, model="gpt-4.1", mcp_url="http://localhost:9000"):
        self.model = model
        self.mcp = MCPHttpClient(mcp_url)
        self.logger = logging.getLogger(__name__)

    def _call_llm(self, messages):
        payload = {
            "model": self.model,
            "messages": messages,
            "tools": TOOLS,
            "tool_choice": "auto",
            "temperature": 0.2,
        }
        resp = post("/chat/completions", payload)
        return resp

    def generate_brief(self, detection_id: str):
        self.sources = {}          # source_id → metadata
        self.source_counter = 1    # s1, s2, s3…

        messages = [
            {"role": "system", "content": INTEL_ANALYST_SYSTEM_PROMPT},
            {"role": "user", "content": f"Write an intelligence brief for detection {detection_id}."}
        ]

        while True:
            llm_response = self._call_llm(messages)
            msg = llm_response["choices"][0]["message"]

            if "tool_calls" in msg:
                messages.append(msg)  # must append assistant message first

                for tool_call in msg["tool_calls"]:
                    tool_name = tool_call["function"]["name"]
                    tool_call_id = tool_call["id"]
                    args = json.loads(tool_call["function"]["arguments"])

                    # Call MCP tool
                    self.logger.info(f"TOOL CALL REQUEST: {tool_name}, args: {args}")
                    raw_result = self.mcp.call_tool(tool_name, args)
                    shrunk_result = self._shrink_tool_result(tool_name, raw_result)

                    self.logger.info(f"TOOL CALL RESULT: {shrunk_result}")

                    tool_payload = self._convert_tool_result_to_sources(tool_name, raw_result)

                    if tool_payload is not None:
                        # One tool message, possibly with many sources inside
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call_id,
                            "content": json.dumps(tool_payload),
                        })
                    else:
                        # Still must respond to the tool call, even if not a "source"
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call_id,
                            "content": json.dumps({
                                "source_id": None,
                                "data": self._sanitize(shrunk_result),
                            }),
                        })

                continue

            final_text = msg["content"]
            used_sources = self._extract_source_ids(final_text)

            final_sources = {
                sid: self.sources[sid]
                for sid in used_sources
                if sid in self.sources
            }

            return {
                "brief": final_text,
                "sources": final_sources
            }

    def _extract_source_ids(self, text):
        ids = re.findall(r"\[(\d+)\]", text)
        return set(ids)
    
    def _convert_tool_result_to_sources(self, tool_name: str, result: Dict[str, Any]) -> Dict[str, Any] | None:
        # get_event → 1 event source
        if tool_name == "get_event":
            sid = self._new_source_id()
            self.sources[sid] = {
                "type": "event",
                "event_id": result["event_id"],
                "title": result.get("title"),
                "summary": result.get("event_summary"),
                "link": f"/events/{result['event_id']}",
            }
            return {
                "sources": [
                    {
                        "source_id": sid,
                        "data": self._sanitize(result),
                    }
                ]
            }

        # get_event_analytics → 1 analytics source
        if tool_name == "get_event_analytics":
            sid = self._new_source_id()
            self.sources[sid] = {
                "type": "event_analytics",
                "event_id": result["event_id"],
                "sentiment": result.get("country_sentiment"),
                "keywords": result.get("country_keywords"),
                "link": f"/events/{result['event_id']}/analytics",
            }
            return {
                "sources": [
                    {
                        "source_id": sid,
                        "data": self._sanitize(result),
                    }
                ]
            }

        # get_articles_for_event → many article sources, but still ONE tool message
        if tool_name == "get_articles_for_event_by_country":
            sources_payload = []
            for article in result.get("articles", [])[:10]:
                sid = self._new_source_id()
                self.sources[sid] = {
                    "type": "article",
                    "article_id": article["article_id"],
                    "title": article["title"],
                    "summary": article.get("summary"),
                    "country": article.get("country"),
                    "clean_description_text": article["clean_description_text"],
                    "clean_body_text": article["clean_body_text"],
                    "sentiment": article.get("sentiment_score"),
                    "keywords": article.get("keyword_list"),
                    "link": f"/articles/{article['article_id']}",
                }
                sources_payload.append({
                    "source_id": sid,
                    "data": self._sanitize(article),
                })

            return {"sources": sources_payload}
        
        if tool_name == "get_detection":
            sid = self._new_source_id()
            self.sources[sid] = {
                'type': 'detection',
                'detection_id': result.get('detection_id'),
                'event_id': result.get("event_id"), 
                'country_code': result.get('country_code'), 
                'detection_type': result.get('detection_type'),
                'timestamp_detected': result.get('timestamp_detected'), 
                'evidence': result.get('evidence')
            }
            return {
                "sources": [
                    {
                        "source_id": sid,
                        "data": self._sanitize(result),
                    }
                ]
            }

        # tools you don't treat as sources
        return None


    def _sanitize(self, obj):
        LARGE_KEYS = {
            "embedding",
            "centroid_embedding",
            "country_embeddings",
            "global_baseline_embedding",
        }

        TRUNCATE_KEYS = {
            "keyword_list",
            "entity_list",
            "country_keywords",
            "global_baseline_keywords",
            "country_entities",
            "global_baseline_entities",
        }

        if isinstance(obj, dict):
            new = {}
            for k, v in obj.items():
                if k in LARGE_KEYS:
                    new[k] = "[omitted: large vector]"
                elif k in TRUNCATE_KEYS and isinstance(v, list):
                    new[k] = v[:5] + ["[... truncated ...]"] if len(v) > 5 else v
                else:
                    new[k] = self._sanitize(v)
            return new

        if isinstance(obj, list):
            return [self._sanitize(x) for x in obj]

        return obj

    def _new_source_id(self):
        sid = f"{self.source_counter}"
        self.source_counter += 1
        return sid

        
    def _shrink_tool_result(self, tool_name: str, result: Dict[str, Any]) -> Dict[str, Any]:
        # Keep detection small – it's already compact
        if tool_name == "get_detection":
            return result

        # Event: keep only what the model needs
        if tool_name == "get_event":
            return {
                "event_id": result.get("event_id"),
                "title": result.get("title"),
                "event_summary": result.get("event_summary"),
                "countries": result.get("countries"),
                "num_articles": result.get("num_articles"),
                "first_seen_at": result.get("first_seen_at"),
                "last_seen_at": result.get("last_seen_at"),
            }

        # Event analytics: drop embeddings entirely, keep only sentiment + maybe keywords
        if tool_name == "get_event_analytics":
            return {
                "event_id": result.get("event_id"),
                "country_sentiment": result.get("country_sentiment"),
                "global_baseline_sentiment": result.get("global_baseline_sentiment"),
                "country_keywords": result.get("country_keywords"),
                "global_baseline_keywords": (result.get("global_baseline_keywords", []))[0:25],
            }

        # Articles: keep only a few articles, and only light fields
        if tool_name == "get_articles_for_event" or tool_name == "search_similar_articles":
            articles = result.get("articles", [])[:10]
            slim = []
            for a in articles:
                slim.append({
                    "article_id": a.get("article_id"),
                    "title": a.get("title"),
                    "summary": a.get("summary"),
                    "clean_description_text": a.get("clean_description_text"),
                    "clean_body_text": a.get("clean_body_text"),
                    "country": a.get("country"),
                    "published_at": a.get("published_at"),
                })
            return {
                "event_id": result.get("event_id"),
                "articles": slim,
            }

        # Similarity searches: keep only ids/titles/distances
        if tool_name in ("search_similar_events", "search_similar_articles"):
            return {
                "results": [
                    {
                        "event_id": r.get("event_id"),
                        "article_id": r.get("article_id"),
                        "title": r.get("title"),
                        "distance": r.get("distance"),
                    }
                    for r in result.get("results", [])[:5]
                ]
            }

        # get_source is already small
        if tool_name == "get_source":
            return result

        return result


        
