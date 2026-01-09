def generate_report(pizzeria):
    return {
        "reserve_left": pizzeria.reserve.current,
        "revenue": pizzeria.ledger.revenue,
        "expenses": pizzeria.ledger.expenses,
        "profit": pizzeria.ledger.profit,
    }
