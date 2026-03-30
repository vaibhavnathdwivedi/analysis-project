import streamlit as st
import pandas as pd
from ai_engine import ask_ai

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("cleaned_superstore_final.csv")

# ----------------------------
# KPI CALCULATIONS
# ----------------------------
category_sales = df.groupby("Category")["Sales"].sum()
category_profit = df.groupby("Category")["Profit"].sum()
category_margin = (category_profit / category_sales)

furniture_margin = category_margin.get("Furniture", 0)
tech_margin = category_margin.get("Technology", 0)

furniture_discount = df[df["Category"] == "Furniture"]["Discount"].mean()
overall_discount = df["Discount"].mean()

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="AI Business Analyst",
    layout="wide",
)

# ----------------------------
# HEADER
# ----------------------------
st.title("📊 AI-Powered Business Decision System")
st.markdown(
    "Analyze business performance using **data + AI insights**. "
    "Select a scenario or ask your own question."
)

# ----------------------------
# QUICK ACTIONS
# ----------------------------
st.markdown("### ⚡ Quick Business Questions")

col1, col2, col3 = st.columns(3)

question = None

with col1:
    if st.button("📉 Why is Furniture less profitable?"):
        question = "Why is Furniture less profitable? Provide detailed reasons."

with col2:
    if st.button("🌍 Which region needs attention?"):
        question = "Which region is underperforming and why? Include risks."

with col3:
    if st.button("💰 How to improve profit?"):
        question = "What specific actions should be taken to improve overall profitability?"

# ----------------------------
# USER INPUT
# ----------------------------
user_input = st.text_input("💬 Ask your own business question:")

if user_input:
    question = user_input

# ----------------------------
# CATEGORY ANALYSIS SECTION
# ----------------------------
st.markdown("---")
st.markdown("### 📊 Category-Level Analysis")

colA, colB = st.columns([2, 1])

with colA:
    selected_category = st.selectbox(
        "Select Category:",
        df["Category"].unique()
    )

with colB:
    analyze_clicked = st.button("🔍 Analyze Selected Category")

# Compute selected category metrics
filtered_df = df[df["Category"] == selected_category]

cat_sales = filtered_df["Sales"].sum()
cat_profit = filtered_df["Profit"].sum()
cat_margin = cat_profit / cat_sales if cat_sales != 0 else 0
cat_discount = filtered_df["Discount"].mean()

# Display category metrics
st.markdown("#### 📌 Selected Category Metrics")

m1, m2, m3 = st.columns(3)

m1.metric("Profit Margin", f"{cat_margin*100:.2f}%")
m2.metric("Total Sales", f"{cat_sales:,.0f}")
m3.metric("Avg Discount", f"{cat_discount*100:.2f}%")

# Generate AI question for category
if analyze_clicked:
    question = f"""
Analyze the performance of {selected_category} category.

Focus on:
- Profitability drivers
- Comparison with other categories
- Risks and inefficiencies
- Growth opportunities
"""

# ----------------------------
# GLOBAL KPI SECTION
# ----------------------------
st.markdown("---")
st.markdown("### 📊 Overall Business KPIs")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Furniture Margin", f"{furniture_margin*100:.1f}%")
k2.metric("Technology Margin", f"{tech_margin*100:.1f}%")
k3.metric("Furniture Discount", f"{furniture_discount*100:.1f}%")
k4.metric("Overall Discount", f"{overall_discount*100:.1f}%")

# ----------------------------
# AI ANALYSIS OUTPUT
# ----------------------------
if question:
    st.markdown("---")
    st.markdown("## 🤖 AI Business Analysis")

    with st.spinner("Analyzing data and generating insights..."):
        answer = ask_ai(question)

    # ----------------------------
    # DISPLAY OUTPUT (FORMATTED)
    # ----------------------------
    st.markdown("### 📌 Key Insight")
    st.success(answer)

    # ----------------------------
    # OPTIONAL: DOWNLOAD REPORT
    # ----------------------------
    st.download_button(
        label="📥 Download Analysis",
        data=answer,
        file_name="ai_business_analysis.txt",
        mime="text/plain"
    )