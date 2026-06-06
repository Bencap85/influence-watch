import logging
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import numpy as np
from pydantic import BaseModel
from mcp.tools import (
    get_detection,
    get_event,
    get_event_analytics,
    get_articles_for_event_by_country,
    get_source,
    search_similar_events,
    search_similar_articles,
)

app = FastAPI()

TOOLS = {
    "get_detection": get_detection,
    "get_event": get_event,
    "get_event_analytics": get_event_analytics,
    "get_articles_for_event_by_country": get_articles_for_event_by_country,
    "get_source": get_source,
    "search_similar_events": search_similar_events,
    "search_similar_articles": search_similar_articles
}

logger = logging.getLogger(__name__)

class ToolCall(BaseModel):
    name: str
    arguments: dict

@app.post("/callTool")
def call_tool(call: ToolCall):

    logger.info(f"Recieved tool call request for tool: {call.name}")
    if call.name not in TOOLS:
        raise HTTPException(status_code=400, detail=f"Unknown tool: {call.name}")

    try:
        result = TOOLS[call.name](**call.arguments)
        
        json_safe = jsonable_encoder(
            result,
            custom_encoder={
                np.float32: float,
                np.float64: float,
                np.int32: int,
                np.int64: int,
            },
        )

        return JSONResponse(content=json_safe)

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))
