import unittest

from tracker import add_expense, total_by_category, total_spent


class TrackerTests(unittest.TestCase):
    def test_add_and_totals(self):
        expenses = []
        add_expense(expenses, 10, "Food")
        add_expense(expenses, 5.5, "food")
        add_expense(expenses, 20, "travel")
        self.assertEqual(total_by_category(expenses), {"food": 15.5, "travel": 20})
        self.assertEqual(total_spent(expenses), 35.5)

    def test_rejects_non_positive_amount(self):
        with self.assertRaises(ValueError):
            add_expense([], 0, "food")


if __name__ == "__main__":
    unittest.main()
