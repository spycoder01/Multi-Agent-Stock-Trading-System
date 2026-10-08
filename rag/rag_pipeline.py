import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from rag.document_loader import load_and_split_pdf
from rag.hybrid_retriever import HybridRetriever


load_dotenv()


class FinancialRAG:

    def __init__(self, pdf_path: str):

        print("Loading financial document...")

        documents = load_and_split_pdf(pdf_path)

        print(f"Created {len(documents)} document chunks.")

        print("Building hybrid retriever...")

        self.retriever = HybridRetriever(documents)

        # LLM configuration
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. "
                "Please check your .env file."
            )

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.6-flash",
            google_api_key=api_key,
            temperature=0.2
        )

    def ask(self, question: str):

        # Retrieve and rerank relevant document chunks
        relevant_docs = self.retriever.retrieve(
            question,
            top_k=3
        )

        if not relevant_docs:
            return "Information not found in the provided document."

        # Build context from retrieved chunks
        context = "\n\n".join(
            doc.page_content
            for doc in relevant_docs
        )

        # Construct the prompt
        prompt = f"""
You are a financial document analysis assistant.

Answer the question using ONLY the information
provided in the context below.

Do not use outside knowledge or invent facts.

If the answer cannot be found in the provided
context, say:

"Information not found in the provided document."

Context:
{context}

Question:
{question}

Provide a concise and accurate answer.
"""

        # Make one Gemini API request
        try:
            response = self.llm.invoke(prompt)
            return response.content

        except Exception as e:

            error_message = str(e)

            if (
                "503" in error_message
                or "UNAVAILABLE" in error_message
            ):
                return (
                    "Financial document analysis is temporarily "
                    "unavailable because Gemini is busy. "
                    "Please try again later."
                )

            raise
