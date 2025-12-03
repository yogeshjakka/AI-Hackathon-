import faiss, numpy as np, pickle, os
class FaissVectorStore:
    def __init__(self, index_path="/mnt/data/faiss.index", dim=384):
        self.index_path = index_path
        self.dim = dim
        try:
            if os.path.exists(index_path):
                self.index = faiss.read_index(index_path)
                with open(index_path+".meta", "rb") as f:
                    self.metadatas = pickle.load(f)
            else:
                raise Exception("No index")
        except Exception:
            self.index = faiss.IndexFlatL2(dim)
            self.metadatas = []

    def add(self, vectors, metadatas):
        arr = np.array(vectors).astype("float32")
        self.index.add(arr)
        self.metadatas.extend(metadatas)
        self._save()

    def search(self, q_vector, top_k=5):
        q = np.array([q_vector]).astype("float32")
        D, I = self.index.search(q, top_k)
        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx == -1: continue
            meta = self.metadatas[idx]
            results.append({"id": idx, "score": float(dist), "metadata": meta, "text": meta.get("text","")})
        return results

    def _save(self):
        import pickle, os
        faiss.write_index(self.index, self.index_path)
        with open(self.index_path+".meta","wb") as f:
            pickle.dump(self.metadatas, f)
