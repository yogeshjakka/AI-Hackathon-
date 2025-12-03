import re
import spacy
from typing import Tuple
nlp = spacy.load("en_core_web_sm")

PHONE_RE = re.compile(r'(\+?\d{1,3}[-.\s]?)?(\d{10})')
EMAIL_RE = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')

def mask_text_for_llm(text: str) -> Tuple[str, dict]:
    tokens = {}
    def em_sub(m):
        t = f"[REDACTED_EMAIL_{len(tokens)}]"
        tokens[t] = m.group(0)
        return t
    text = EMAIL_RE.sub(em_sub, text)

    def ph_sub(m):
        t = f"[REDACTED_PHONE_{len(tokens)}]"
        tokens[t] = m.group(0)
        return t
    text = PHONE_RE.sub(ph_sub, text)

    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ("PERSON","GPE","LOC","ADDRESS"):
            tag = f"[REDACTED_{ent.label_}_{len(tokens)}]"
            tokens[tag] = ent.text
            text = text.replace(ent.text, tag)

    return text, tokens

def post_llm_contains_pii(text: str) -> bool:
    if EMAIL_RE.search(text): return True
    if re.search(r'\+?\d{6,}', text): return True
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ("PERSON","GPE","LOC","ADDRESS"):
            if "REDACTED" not in ent.text:
                return True
    return False
