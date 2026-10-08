from crew import create_crew


if __name__ == "__main__":

    stock_symbol = input(
        "Enter stock symbol (e.g., AAPL or BMW.DE): "
    ).strip()

    pdf_path = input(
        "Enter company PDF path "
        "(optional, press Enter to skip): "
    ).strip()

    if pdf_path:

        print("\nFinancial document provided.")
        print("Financial RAG enabled.")

    else:

        print("\nNo financial document provided.")
        print("Financial RAG disabled.")

    crew = create_crew(pdf_path)

    result = crew.kickoff(
        inputs={
            "stock_symbol": stock_symbol
        }
    )

    print("\n\n==============================")
    print("FINAL TRADING RECOMMENDATION")
    print("==============================\n")

    print(result)