from fastapi import FastAPI
from backend.app.api import chat, tools

app = FastAPI(title="Hyper-Personalized Support API")
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(tools.router, prefix="/tools", tags=["tools"])

@app.get("/")
def health():
    return {"status":"ok"}
