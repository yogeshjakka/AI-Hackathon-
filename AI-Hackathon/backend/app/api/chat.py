from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.core.pii_masker import mask_text_for_llm, post_llm_contains_pii
from backend.app.core.rag import retrieve_grounding
from backend.app.core.llm_client import call_llm, validate_numbers_in_llm_reply
from backend.app.api.tools import call_tool_inventory, call_tool_coupon
from typing import Optional

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    message: str
    location: Optional[dict] = None  # {"lat":.., "lon":..}

class ChatResponse(BaseModel):
    reply: str
    sources: list

@router.post("/message", response_model=ChatResponse)
async def message(req: ChatRequest):
    # mask input PII
    masked_message, tokens = mask_text_for_llm(req.message)

    # create retrieval query from masked_message + context
    retrieved = retrieve_grounding(masked_message, location=req.location)

    # check quick tool interactions (example: user near store -> check inventory)
    inventory = None
    coupon = None
    if "cold" in masked_message.lower():
        store_id = retrieved.get("nearest_store_id")
        if store_id:
            inventory = await call_tool_inventory(store_id, "Hot Cocoa")
            coupon = await call_tool_coupon(req.user_id or "anon", store_id)

    # prepare LLM prompt context
    system_ctx = {
        "intent": "customer_support",
        "masked_tokens": tokens,
        "tools": {"inventory": inventory, "coupon": coupon},
        "retrieved": retrieved.get("docs_snippets", [])
    }

    # call the LLM (we pass masked context; llm_client handles sending)
    llm_resp = await call_llm(system_ctx, masked_message)

    # validate numbers: ensure any numeric claims match retrieved tool results
    if not validate_numbers_in_llm_reply(llm_resp.get("text",""), inventory):
        raise HTTPException(status_code=500, detail="LLM numeric validation failed.")

    # final PII check of the LLM output
    if post_llm_contains_pii(llm_resp.get("text","")):
        raise HTTPException(status_code=500, detail="PII detected in LLM output (post-check).")

    return ChatResponse(reply=llm_resp.get("text",""), sources=[d.get("id") for d in retrieved.get("docs_snippets",[])])
