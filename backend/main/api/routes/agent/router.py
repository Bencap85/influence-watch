import os
import uuid
import logging
from dotenv import load_dotenv
from fastapi import APIRouter
from main.agent.analyst_agent import AnalystAgent

logger = logging.getLogger(__name__)

router = APIRouter()

mcp_url = os.getenv("MCP_SERVER_BASE_URL")

if not mcp_url:
    logger.info("MCP URL not found! Unable to start")
    exit(1)

agent = AnalystAgent(mcp_url=mcp_url)

@router.get("/agent/brief/{detection_id}")
async def intel_brief(detection_id: str):
    summary = agent.generate_brief(str(detection_id))
    return {"detection_id": detection_id, "brief": summary}
