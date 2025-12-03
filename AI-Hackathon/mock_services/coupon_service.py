from fastapi import FastAPI
import uvicorn
app = FastAPI()

@app.get("/coupon/{user_id}/{store_id}")
def get_coupon(user_id: str, store_id: str):
    return {"eligible": True, "code": "HOTCOCOA10", "discount": 10, "expires": "2025-12-31"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8102)
