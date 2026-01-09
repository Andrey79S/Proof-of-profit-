def generate_report(ledger):
    return {
        "revenue": ledger.revenue,
        "expenses": ledger.expenses,
        "profit": ledger.profit,
    }
