TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_detection",
            "description": "Retrieve a detection record by detection_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "detection_id": {"type": "string"}
                },
                "required": ["detection_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_event",
            "description": "Retrieve event metadata and summary information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {"type": "string"}
                },
                "required": ["event_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_event_analytics",
            "description": "Retrieve analytics for an event, including embeddings, keywords, entities, and sentiment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {"type": "string"}
                },
                "required": ["event_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_articles_for_event_by_country",
            "description": "Retrieve processed articles associated with an event by a particular country.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {"type": "string"},
                    "country": {"type": "string"}
                },
                "required": ["event_id", "country"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_source",
            "description": "Retrieve metadata about a source by source_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_id": {"type": "integer"}
                },
                "required": ["source_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_similar_events",
            "description": "Search for events similar to a given event.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {"type": "string"},
                    "limit": {"type": "integer"}
                },
                "required": ["event_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_similar_articles",
            "description": "Search for articles similar to a given article.",
            "parameters": {
                "type": "object",
                "properties": {
                    
                    "article_id": {"type": "string"},
                    "limit": {"type": "integer"}
                },
                "required": ["embedding"]
            }
        }
    }
]