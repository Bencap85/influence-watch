import os
import time
import random
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = "https://api.openai.com/v1"

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
}

logger = logging.getLogger(__name__)

def post(path: str, payload: dict):
    url = f"https://api.openai.com/v1{path}"
    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code >= 400:
        logger.error("OPENAI ERROR %s:\n%s", response.status_code, response.text)
        # DO NOT raise yet — return the body so we can inspect it
        raise requests.exceptions.HTTPError(
            f"OpenAI returned {response.status_code}: {response.text}",
            response=response
        )

    return response.json()
