from fastapi import FastAPI
import uvicorn
app = FastAPI()

DATA = {
    "STARB_1": {"Hot Cocoa": {"available": True, "qty": 12}, "Latte": {"available": True, "qty": 3}},
    "COFFEE_2": {"Hot Cocoa": {"available": False, "qty": 0}}
}

@app.get("/inventory/{store_id}/{sku}")
def get_inventory(store_id: str, sku: str):
    store = DATA.get(store_id, {})
    item = store.get(sku, {"available": False, "qty": 0})
    return {"store_id": store_id, "sku": sku, **item}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8101)
