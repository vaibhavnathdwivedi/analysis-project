import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("cleaned_superstore_final.csv")

# ----------------------------
# KPI CALCULATIONS
# ----------------------------
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()

category_sales = df.groupby("Category")["Sales"].sum()
category_profit = df.groupby("Category")["Profit"].sum()
category_margin = (category_profit / category_sales)

furniture_margin = category_margin.get("Furniture", 0)
tech_margin = category_margin.get("Technology", 0)

furniture_discount = df[df["Category"] == "Furniture"]["Discount"].mean()
overall_discount = df["Discount"].mean()

top_category = category_sales.idxmax()
low_profit_category = category_profit.idxmin()
top_region = df.groupby("Region")["Sales"].sum().idxmax()

# ----------------------------
# AUTOMATED DETECTION
# ----------------------------
insights = []

if furniture_margin < 0.05:
    insights.append("Furniture category has critically low profit margin.")

if furniture_discount > overall_discount:
    insights.append("Furniture discount is higher than overall average, impacting profit.")

if low_profit_category == "Furniture":
    insights.append("Furniture is the lowest profit category.")

auto_insights = "\n".join(insights)

# ----------------------------
# DECISION ENGINE
# ----------------------------
decisions = []

if furniture_margin < 0.05:
    decisions.append("Increase pricing or reduce costs in Furniture category.")

if furniture_discount > overall_discount:
    decisions.append("Reduce discount levels for Furniture products.")

decision_summary = "\n".join(decisions)

# ----------------------------
# STRUCTURED SUMMARY
# ----------------------------
summary = f"""
Business Metrics:

Total Sales: {total_sales:.2f}
Total Profit: {total_profit:.2f}

Category Performance:
Furniture Margin: {furniture_margin*100:.2f}%
Technology Margin: {tech_margin*100:.2f}%

Discount Analysis:
Furniture Discount: {furniture_discount*100:.2f}%
Overall Discount: {overall_discount*100:.2f}%

Top Category: {top_category}
Lowest Profit Category: {low_profit_category}
Top Region: {top_region}

Automated Findings:
{auto_insights}

Recommended Actions:
{decision_summary}
"""

# ----------------------------
# GEMINI SETUP
# ----------------------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


# ----------------------------
# AI FUNCTION
# ----------------------------
def ask_ai(question):
    response = model.generate_content(
        f"""
You are a senior business analyst.

STRICT RULES:
- Use ONLY the data provided
- MUST include numbers
- MUST explain WHY (not just WHAT)
- Recommendations must be SPECIFIC and actionable

DATA:
{summary}

QUESTION:
{question}

OUTPUT FORMAT:

Key Insight:
- Data-backed insight with numbers

Root Cause:
- Explain underlying drivers (discounts, margins, etc.)

Recommendation:
- Specific actions (pricing, discount, strategy)
"""
    )

    return response.text