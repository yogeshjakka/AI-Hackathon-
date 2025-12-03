import os
from sentence_transformers import SentenceTransformer
from backend.app.utils.faiss_store import FaissVectorStore
from pathlib import Path

EMBED_MODEL = os.environ.get("EMBEDDING_MODEL","sentence-transformers/all-MiniLM-L6-v2")
embedder = SentenceTransformer(EMBED_MODEL)
store = FaissVectorStore(index_path=os.environ.get("FAISS_INDEX_PATH","/mnt/data/faiss.index"))

def chunk_text(text, chunk_size=400, overlap=100):
    tokens = text.split()
    start = 0
    chunks = []
    while start < len(tokens):
        chunk = " ".join(tokens[start:start+chunk_size])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def ingest_folder(folder_path="./backend/documents"):
    metas = []
    vecs = []
    for p in Path(folder_path).glob("**/*"):
        if p.is_file() and p.suffix.lower() in (".txt", ".md"):
            text = p.read_text(encoding="utf-8")
            chunks = chunk_text(text)
            for i,c in enumerate(chunks):
                vec = embedder.encode([c])[0]
                meta = {"path": str(p), "chunk": i, "title": p.name, "text": c, "store_id": None}
                metas.append(meta)
                vecs.append(vec)
    if vecs:
        store.add(vecs, metas)
    print(f"Ingested {len(vecs)} chunks")

if __name__ == "__main__":
    ingest_folder()
