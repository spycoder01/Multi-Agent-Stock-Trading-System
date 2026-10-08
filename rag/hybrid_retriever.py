from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever

from sentence_transformers import CrossEncoder


class HybridRetriever:

    def __init__(self, documents):

        self.documents = documents

        # -------------------------
        # FAISS
        # -------------------------

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vector_store = FAISS.from_documents(
            documents,
            self.embeddings
        )

        self.faiss_retriever = (
            self.vector_store.as_retriever(
                search_kwargs={"k": 15}
            )
        )

        # -------------------------
        # BM25
        # -------------------------

        self.bm25_retriever = BM25Retriever.from_documents(
            documents
        )

        self.bm25_retriever.k = 15

        # -------------------------
        # Cross Encoder
        # -------------------------

        self.reranker = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )


    def retrieve(self, query, top_k=3):

        # FAISS retrieval
        faiss_docs = self.faiss_retriever.invoke(query)

        # BM25 retrieval
        bm25_docs = self.bm25_retriever.invoke(query)

        # --------------------------------
        # Combine candidates
        # --------------------------------

        candidates = faiss_docs + bm25_docs

        # Remove duplicate chunks
        unique_candidates = {}

        for doc in candidates:

            content = doc.page_content

            if content not in unique_candidates:
                unique_candidates[content] = doc

        candidates = list(unique_candidates.values())

        # --------------------------------
        # CrossEncoder reranking
        # --------------------------------

        pairs = [
            [query, doc.page_content]
            for doc in candidates
        ]

        scores = self.reranker.predict(pairs)

        ranked_docs = sorted(
            zip(candidates, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            doc
            for doc, score in ranked_docs[:top_k]
        ]