from crew import crew


if __name__ == "__main__":

    stock_symbol = input(
        "Enter stock symbol (e.g., AAPL or RELIANCE.NS): "
    ).strip()

    result = crew.kickoff(
        inputs={
            "stock_symbol": stock_symbol
        }
    )

    print("\n\n==============================")
    print("FINAL TRADING RECOMMENDATION")
    print("==============================\n")

    print(result)