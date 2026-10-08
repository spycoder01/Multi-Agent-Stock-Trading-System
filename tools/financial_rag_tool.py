import os

from crewai.tools import tool

from rag.rag_pipeline import FinancialRAG


@tool("Financial Document Research Tool")
def get_financial_document_analysis(
    question: str,
    pdf_path: str
) -> str:
    """
    Analyze a company financial document using the Financial RAG pipeline.
    """

    if not pdf_path:
        return "No financial document was provided."

    if not os.path.exists(pdf_path):
        return f"Financial document not found: {pdf_path}"

    try:
        rag = FinancialRAG(pdf_path)

        answer = rag.ask(question)

        # Extract text from LLM's structured response
        if isinstance(answer, list):
            for item in answer:
                if isinstance(item, dict) and item.get("type") == "text":
                    return item.get("text", "")

        return str(answer)

    except Exception as e:
        return f"Financial document analysis failed: {str(e)}"