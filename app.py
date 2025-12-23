import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Smart Student Expense Assistant",
    page_icon="🎓",
    layout="wide"
)

DATA_FILE = "expenses.csv"

# ---------------- STYLES ----------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.big-title {
    font-size: 42px;
    font-weight: 800;
}
.subtle {
    color: #b0b0b0;
}
.card {
    background: #161b22;
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA UTILS ----------------
def load_data():
    try:
        return pd.read_csv(DATA_FILE)
    except:
        return pd.DataFrame(columns=["date", "amount", "category", "note"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# ---------------- LOAD DATA ----------------
df = load_data()

# ---------------- HEADER ----------------
st.markdown('<div class="big-title">🎓 Smart Student Expense & Budget Assistant</div>', unsafe_allow_html=True)
st.markdown(
    "Helping students build **financial awareness**, control spending, and develop **budgeting discipline** early. 💡",
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.header("💰 Monthly Budget")
budget = st.sidebar.number_input("Enter your monthly budget (₹)", min_value=0.0, step=500.0)

# ---------------- ADD EXPENSE ----------------
st.markdown("## ➕ Add New Expense")

with st.container():
    col1, col2, col3 = st.columns(3)

    with col1:
        amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)

    with col2:
        category = st.selectbox(
            "Category",
            ["🍔 Food", "🚕 Travel", "📚 Study", "🎮 Entertainment", "🏋️ Gym", "💡 Other"]
        )

    with col3:
        note = st.text_input("Note (optional)")

    if st.button("Add Expense"):
        new_row = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "amount": amount,
            "category": category,
            "note": note
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success("✅ Expense added successfully!")

st.markdown("---")

# ---------------- SUMMARY ----------------
st.markdown("## 📊 Expense Summary")

total_spent = df["amount"].sum()
st.metric("Total Spent (₹)", f"{total_spent:.2f}")

# Budget Progress
if budget > 0:
    progress = min(total_spent / budget, 1.0)
    st.progress(progress)
    st.caption(f"₹{max(budget - total_spent, 0):.2f} remaining")

# ---------------- CATEGORY PIE ----------------
if not df.empty:
    st.markdown("### 🧩 Category-wise Spending")
    category_totals = df.groupby("category")["amount"].sum()

    fig1, ax1 = plt.subplots()
    ax1.pie(category_totals, labels=category_totals.index, autopct="%1.1f%%")
    ax1.axis("equal")
    st.pyplot(fig1)

# ---------------- DAILY TREND ----------------
if not df.empty:
    st.markdown("### 📈 Daily Spending Trend")
    daily = df.groupby("date")["amount"].sum()

    fig2, ax2 = plt.subplots()
    ax2.plot(daily.index, daily.values, marker="o")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Amount (₹)")
    st.pyplot(fig2)

# ---------------- SMART INSIGHTS ----------------
st.markdown("## 💡 Smart Insights")

if not df.empty:
    max_cat = category_totals.idxmax()
    st.info(f"🔍 You spent most on **{max_cat}**.")

    if budget > 0 and total_spent > budget:
        st.warning("⚠️ You have exceeded your monthly budget!")

    if category_totals[max_cat] > 0.4 * total_spent:
        st.info(f"📌 **{max_cat}** is taking a large portion of your spending.")

else:
    st.info("No expenses recorded yet.")

# ---------------- EXPORT REPORT ----------------
st.markdown("## 📄 Export Monthly Summary")

if st.button("Download Report"):
    report = f"""
SMART STUDENT EXPENSE REPORT
----------------------------
Total Spent: ₹{total_spent:.2f}
Highest Category: {max_cat if not df.empty else 'N/A'}
Remaining Budget: ₹{max(budget - total_spent, 0):.2f}

Generated on: {datetime.now().strftime('%d %B %Y')}
"""
    st.download_button("📥 Download Text Report", report)
    st.success("✅ Report generated successfully!")