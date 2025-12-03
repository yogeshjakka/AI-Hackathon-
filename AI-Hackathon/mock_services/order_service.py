from fastapi import FastAPI
import uvicorn
app = FastAPI()
ORDERS = {
    "user_1": {"order_id":"ORD123","status":"out_for_delivery"}
}
@app.get("/order/{user_id}")
def get_order(user_id: str):
    return ORDERS.get(user_id, {})
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8103)
