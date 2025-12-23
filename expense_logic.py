import csv
from datetime import datetime
import os

FILE_NAME = "expenses.csv"

# ---------- INITIALIZE FILE ----------
def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "amount", "category", "note"])


# ---------- ADD EXPENSE ----------
def add_expense(amount, category, note=""):
    date = datetime.now().strftime("%Y-%m-%d")
    with open(FILE_NAME, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, amount, category, note])


# ---------- READ ALL EXPENSES ----------
def read_expenses():
    expenses = []
    if not os.path.exists(FILE_NAME):
        return expenses

    with open(FILE_NAME, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["amount"] = float(row["amount"])
            expenses.append(row)
    return expenses


# ---------- CALCULATIONS ----------
def get_total_spent(expenses):
    return sum(e["amount"] for e in expenses)


def category_summary(expenses):
    summary = {}
    for e in expenses:
        summary[e["category"]] = summary.get(e["category"], 0) + e["amount"]
    return summary


def daily_spending(expenses):
    daily = {}
    for e in expenses:
        daily[e["date"]] = daily.get(e["date"], 0) + e["amount"]
    return daily


def get_insights(expenses):
    if not expenses:
        return []

    summary = category_summary(expenses)
    highest_category = max(summary, key=summary.get)

    insights = []
    insights.append(f"You spent most on **{highest_category}**.")
    insights.append(f"Total expenses recorded: ₹{get_total_spent(expenses):.2f}")
    return insights
