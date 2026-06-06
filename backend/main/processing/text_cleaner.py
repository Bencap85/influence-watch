from typing import List

from bs4 import BeautifulSoup

def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def clean_html(html: str | None) -> str:
    if not html:
        return ""
    return extract_text(html)

def strip_metadata(text: str, meta_phrases: List[str]) -> str:
    for phrase in meta_phrases:
        text = text.replace(phrase, "")

    return text
