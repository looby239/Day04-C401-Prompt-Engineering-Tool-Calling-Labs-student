from __future__ import annotations
from typing import Any
import requests
from tools._shared import TIMEOUT, err

def translate_text(text: str = "", target_lang: str = "vi", source_lang: str = "auto") -> dict[str, Any]:
    """
    Translate text from source_lang to target_lang using Google Translate API.
    """
    if not text:
        return {"tool": "translate", "translated_text": "", "source_lang": source_lang, "target_lang": target_lang}
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": source_lang,
            "tl": target_lang,
            "dt": "t",
            "q": text
        }
        resp = requests.get(url, params=params, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        translated = "".join([sentence[0] for sentence in data[0] if sentence[0]])
        return {
            "tool": "translate",
            "original_text": text,
            "translated_text": translated,
            "source_lang": source_lang,
            "target_lang": target_lang
        }
    except Exception as exc:
        return err("translate", exc)
