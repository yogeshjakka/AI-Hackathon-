from backend.app.utils.faiss_store import FaissVectorStore
from sentence_transformers import SentenceTransformer
import os
EMBED_MODEL = os.environ.get("EMBEDDING_MODEL","sentence-transformers/all-MiniLM-L6-v2")
embedder = SentenceTransformer(EMBED_MODEL)
store = FaissVectorStore(index_path=os.environ.get("FAISS_INDEX_PATH","/mnt/data/faiss.index"))

def retrieve_grounding(query: str, location: dict=None, top_k:int=5):
    q_emb = embedder.encode([query])[0]
    hits = store.search(q_emb, top_k=top_k)
    nearest_store_id = None
    for h in hits:
        meta = h.get("metadata",{})
        if meta.get("store_id"):
            nearest_store_id = meta.get("store_id")
            break
    return {"docs_snippets": hits, "nearest_store_id": nearest_store_id}
