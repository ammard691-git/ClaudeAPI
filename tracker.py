import json
from datetime import date
from pathlib import Path

DATA_FILE = Path("expenses.json")


def load_expenses(path=DATA_FILE):
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save_expenses(expenses, path=DATA_FILE):
    path.write_text(json.dumps(expenses, indent=2), encoding="utf-8")


def add_expense(expenses, amount, category, note=""):
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    expense = {
        "date": date.today().isoformat(),
        "amount": round(amount, 2),
        "category": category.lower(),
        "note": note,
    }
    expenses.append(expense)
    return expense


def total_by_category(expenses):
    totals = {}
    for e in expenses:
        totals[e["category"]] = round(totals.get(e["category"], 0) + e["amount"], 2)
    return totals


def total_spent(expenses):
    return round(sum(e["amount"] for e in expenses), 2)
