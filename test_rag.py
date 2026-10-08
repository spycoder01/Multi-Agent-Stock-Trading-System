from rag.rag_pipeline import FinancialRAG

PDF_PATH = "documents/BMW_report.pdf"

rag = FinancialRAG(PDF_PATH)

while True:

    question = input(
        "\nAsk a question (type 'exit' to quit): "
    )

    if question.lower() == "exit":
        break

    answer = rag.ask(question)

    print("\n==============================")
    print("ANSWER")
    print("==============================")

    print(answer)