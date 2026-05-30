from workflow.graph import app

initial_state = {
    "stock_symbol": "TSLA"
}

result = app.invoke(initial_state)

print("\n===== FINAL OUTPUT =====\n")

print(result["strategy"])