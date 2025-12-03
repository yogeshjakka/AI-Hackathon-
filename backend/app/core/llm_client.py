import os, httpx
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = os.environ.get("MODEL","gpt-4o-mini")

async def call_llm(system_ctx: dict, user_message: str):
    prompt = build_prompt(system_ctx, user_message)
    headers = {"Authorization": f"Bearer {OPENAI_KEY}"}
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post("https://api.openai.com/v1/chat/completions", json={
            "model": MODEL,
            "messages": [
                {"role":"system","content":"You are a customer support assistant. Only use provided retrieved docs and tools. If not sure say 'Unknown'."},
                {"role":"user","content": prompt}
            ],
            "max_tokens": 300
        }, headers=headers)
        data = resp.json()
        text = data.get("choices",[])[0].get("message",{}).get("content","") if data.get("choices") else ""
    return {"text": text, "raw": data}

def build_prompt(system_ctx, user_message):
    ctx = [f"USER_MESSAGE: {user_message}", f"TOOLS: {system_ctx.get('tools')}", "RETRIEVED_DOCS:"]
    for d in system_ctx.get("retrieved", []):
        ctx.append(f"- {d.get('text')[:400]}  (id:{d.get('id')})")
    ctx.append("Write a short helpful reply. If any number or inventory statement is included ensure it's verified by tools. If you cannot verify, say 'Unknown'.")
    return "\n".join(ctx)

def validate_numbers_in_llm_reply(reply_text: str, inventory_result: dict) -> bool:
    if inventory_result is None:
        return True
    claimed_in_stock = "in stock" in reply_text.lower() or "available" in reply_text.lower()
    if claimed_in_stock and not inventory_result.get("available", False):
        return False
    return True
