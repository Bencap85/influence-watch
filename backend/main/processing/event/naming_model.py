import json
import logging
from main.processing.openai_http import post


class NamingModel:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def build_prompt(self, event_to_headlines: dict[int, list[str]]) -> str:
        prompt = """
        You generate concise event titles.

        Input: a mapping of event IDs → lists of 1–5 headlines describing the same event.

        Output: a JSON object where each key is an event ID (as a string) and each value is a short, neutral title summarizing the event.

        Rules:
        - Max 12 words per title
        - No sensational language
        - Do not copy headlines verbatim
        - Focus on the shared theme
        - Focus on the underlying event, NOT the reporting about it.
        - Avoid meta-journalistic words such as: “perspective”, “take”, “coverage”, “report”, “analysis”, “opinion”, “reaction”, "insight into", "examining", etc.
        - Describe what actually happened in the world: actions, decisions, announcements, incidents, discoveries, agreements, conflicts, etc.
        - Output ONLY valid JSON, like:
        {
            "123": "Short title",
            "456": "Another title"
        }

        Events:
        """
        for event_id, headlines in event_to_headlines.items():
            prompt += f'\nEvent {event_id}:\n'
            for h in headlines:
                prompt += f"- {h}\n"

        return prompt

    def generate_event_titles(self, event_to_headlines: dict) -> dict: 
        # prompt = self.build_prompt(event_to_headlines)
        # client = get_openai_client()

        # response = client.chat.completions.create( 
        #     model="gpt-4o-mini", 
        #     messages=[{"role": "user", "content": prompt}], 
        #     response_format={"type": "json_object"}
        # )

        # raw = response.choices[0].message.content
        # data = json.loads(raw)
        # # Convert ids to ints
        # return {int(k): v for k, v in data.items()}
        self.logger.info(f"Calling LLM to name {len(event_to_headlines.keys())} events...")
        prompt = self.build_prompt(event_to_headlines)

        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"},
        }

        data = post("/chat/completions", payload)
        raw = data["choices"][0]["message"]["content"]
        parsed = json.loads(raw)
        return {k: v for k, v in parsed.items()}
