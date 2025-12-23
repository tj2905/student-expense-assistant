import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from expense_logic import (
    initialize_file,
    add_expense,
    read_expenses,
    get_total_spent,
    category_summary,
    daily_spending,
    get_insights,
)

# ---------- PAGE SETUP ----------
st.set_page_config(page_title="Student Expense Assistant", layout="centered")
st.title("🎓 Smart Student Expense & Budget Assistant")

initialize_file()

# ---------- SIDEBAR ----------
st.sidebar.header("Monthly Budget")
budget = st.sidebar.number_input("Enter your monthly budget (₹)", min_value=0.0)

# ---------- ADD EXPENSE ----------
st.subheader("➕ Add New Expense")
amount = st.number_input("Amount (₹)", min_value=0.0)
category = st.selectbox(
    "Category", ["Food", "Travel", "Study", "Entertainment", "Others"]
)
note = st.text_input("Note (optional)")

if st.button("Add Expense"):
    if amount > 0:
        add_expense(amount, category, note)
        st.success("Expense added successfully!")
    else:
        st.error("Please enter a valid amount.")

# ---------- LOAD DATA ----------
expenses = read_expenses()

if expenses:
    df = pd.DataFrame(expenses)

    # ---------- SUMMARY ----------
    st.subheader("📊 Expense Summary")
    total_spent = get_total_spent(expenses)
    st.metric("Total Spent (₹)", f"{total_spent:.2f}")

    if budget > 0:
        remaining = budget - total_spent
        st.metric("Remaining Budget (₹)", f"{remaining:.2f}")

    # ---------- PIE CHART ----------
    st.subheader("🧩 Category-wise Spending")
    cat_data = category_summary(expenses)
    fig1, ax1 = plt.subplots()
    ax1.pie(cat_data.values(), labels=cat_data.keys(), autopct="%1.1f%%")
    st.pyplot(fig1)

    # ---------- LINE CHART ----------
    st.subheader("📈 Daily Spending Trend")
    daily_data = daily_spending(expenses)
    daily_df = pd.DataFrame(
        list(daily_data.items()), columns=["Date", "Amount"]
    ).sort_values("Date")
    st.line_chart(daily_df.set_index("Date"))

    # ---------- INSIGHTS ----------
    st.subheader("💡 Smart Insights")
    for insight in get_insights(expenses):
        st.write("•", insight)

else:
    st.info("No expenses added yet. Start by adding one above!")
