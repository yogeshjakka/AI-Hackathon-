from fastapi import APIRouter
import httpx
router = APIRouter()

INVENTORY_URL = "http://localhost:8101"
COUPON_URL = "http://localhost:8102"
ORDER_URL = "http://localhost:8103"

async def call_tool_inventory(store_id: str, sku: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{INVENTORY_URL}/inventory/{store_id}/{sku}")
        return resp.json()

async def call_tool_coupon(user_id: str, store_id: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{COUPON_URL}/coupon/{user_id}/{store_id}")
        return resp.json()

@router.get("/health")
async def health():
    return {"tools":"ok"}
