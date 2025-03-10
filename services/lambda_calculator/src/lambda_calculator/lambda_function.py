def lambda_handler() -> dict:
    try:
        cagr = 0.1
        volatility = 0.2
        sharpe_ratio = cagr / volatility
        performance = {"cagr": cagr, "volatility": volatility, "sharpe_ratio": sharpe_ratio}

        return performance

    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    lambda_handler()
