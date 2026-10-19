import argparse

from tracker import (
    add_expense,
    load_expenses,
    save_expenses,
    total_by_category,
    total_spent,
)


def main():
    parser = argparse.ArgumentParser(description="Simple expense tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Add an expense")
    add.add_argument("amount", type=float)
    add.add_argument("category")
    add.add_argument("--note", default="")

    sub.add_parser("list", help="List all expenses")
    sub.add_parser("summary", help="Show totals by category")

    args = parser.parse_args()
    expenses = load_expenses()

    if args.command == "add":
        try:
            e = add_expense(expenses, args.amount, args.category, args.note)
        except ValueError as err:
            parser.error(str(err))
        save_expenses(expenses)
        print(f"Added {e['amount']} to {e['category']}")
    elif args.command == "list":
        for e in expenses:
            print(f"{e['date']}  {e['amount']:>8.2f}  {e['category']:<10} {e['note']}")
    elif args.command == "summary":
        for cat, total in sorted(total_by_category(expenses).items()):
            print(f"{cat:<10} {total:>8.2f}")
        print(f"{'TOTAL':<10} {total_spent(expenses):>8.2f}")


if __name__ == "__main__":
    main()
