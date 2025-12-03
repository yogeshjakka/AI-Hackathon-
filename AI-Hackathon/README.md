# Hyper-Personalized Customer Support Agent

Production-grade, backend-first prototype of a context-aware conversational AI with:
- RAG (FAISS embeddings)
- PII masking (regex + spaCy)
- Deterministic tool layer (inventory, coupon, order)
- LLM orchestration with numeric validation and grounding

## How to Run

1. Clone repo (or download ZIP)
2. Create and activate a Python 3.11+ virtualenv
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create `.env` from `.env.example` and fill keys.
5. Ingest documents:
   ```bash
   python backend/app/ingestion/ingest_documents.py
   ```
6. Start mock services (optional in separate terminals):
   ```bash
   uvicorn mock_services.inventory_service:app --port 8101
   uvicorn mock_services.coupon_service:app --port 8102
   uvicorn mock_services.order_service:app --port 8103
   ```
7. Run backend:
   ```bash
   uvicorn backend.app.main:app --reload --port 8000
   ```
8. Open frontend:
   Open `frontend/public/index.html` in your browser and test.

## Notes
- This prototype uses an OpenAI-style endpoint. Adapt `backend/app/core/llm_client.py` to your provider (Vertex/Gemini).
- Place text versions of policy docs under `backend/documents/` before ingesting.
