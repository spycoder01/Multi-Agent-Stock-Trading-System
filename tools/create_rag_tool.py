import os

from crewai.tools import tool

from rag.rag_pipeline import FinancialRAG


def create_financial_rag_tool(pdf_path):

    if not pdf_path:
        return None

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(
            f"Financial document not found: {pdf_path}"
        )

    print("\nLoading financial document for RAG...")

    rag = FinancialRAG(pdf_path)

    @tool("Financial Document Research Tool")
    def financial_document_research(question: str) -> str:
        """
        Search the provided company financial document and answer
        questions using the Financial RAG pipeline.
        """

        try:

            answer = rag.ask(question)

            # Handle LLM structured response
            if isinstance(answer, list):

                for item in answer:

                    if (
                        isinstance(item, dict)
                        and item.get("type") == "text"
                    ):
                        return item.get("text", "")

            return str(answer)

        except Exception as e:

            return (
                f"Financial document analysis failed: {str(e)}"
            )

    return financial_document_research