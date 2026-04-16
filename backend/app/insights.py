from __future__ import annotations

from typing import Dict, Any, List

SAVINGS_RATE_WARNING = 20
HIGH_CATEGORY_PERCENT = 30
FOOD_THRESHOLD = 2000
SHOPPING_THRESHOLD = 1000


def generate_insights(summary: Dict[str, Any]) -> List[str]:
    """Generate human-readable insights from financial summary data."""
    insights: List[str] = []

    total_income = summary.get("total_income", 0.0)
    total_expense = summary.get("total_expense", 0.0)
    balance = summary.get("balance", 0.0)
    top_category = summary.get("top_category")
    top_category_amount = summary.get("top_category_amount", 0.0)
    category_breakdown = summary.get("category_breakdown", {})

    if total_income == 0:
        insights.append("No income was recorded. Savings and budgeting analysis may be incomplete.")

    if total_expense > total_income and total_income > 0:
        insights.append("You are spending more than you earn. This is a warning sign for your cash flow.")

    if balance < 0:
        insights.append(f"You are currently running a deficit of ₹{abs(balance):.2f}.")

    if total_income > 0:
        savings_rate = (balance / total_income) * 100
        insights.append(f"Your current savings rate is {savings_rate:.2f}%.")

        if savings_rate < SAVINGS_RATE_WARNING:
            insights.append("Your savings rate is below 20%. Consider reducing non-essential expenses.")
        else:
            insights.append("Your savings rate looks healthy.")

    if top_category:
        insights.append(
            f"Your highest spending category is '{top_category}' with ₹{top_category_amount:.2f} spent."
        )

    if total_expense > 0:
        for category, amount in category_breakdown.items():
            percent = (amount / total_expense) * 100
            if percent >= HIGH_CATEGORY_PERCENT:
                insights.append(
                    f"'{category}' takes {percent:.2f}% of your expenses, which is quite high."
                )

    if category_breakdown.get("food", 0) > FOOD_THRESHOLD:
        insights.append("Food spending is noticeably high. Check if frequent ordering is increasing your expenses.")

    if category_breakdown.get("shopping", 0) > SHOPPING_THRESHOLD:
        insights.append("Shopping expenses are significant. Review whether these purchases were necessary.")

    if not insights:
        insights.append("Your data looks stable, but more transactions will give better insights.")

    return insights


def build_ai_prompt(summary: Dict[str, Any], insights: List[str]) -> str:
    """Prepare a prompt that can later be sent to an LLM like Grok."""
    category_breakdown = summary.get("category_breakdown", {})

    category_lines = "\n".join(
        f"- {category}: ₹{amount:.2f}"
        for category, amount in category_breakdown.items()
    ) or "- No category data available"

    insight_lines = "\n".join(f"- {insight}" for insight in insights) or "- No insights generated"

    prompt = f"""
You are a personal finance assistant.

Here is the financial summary:
- Total income: ₹{summary.get('total_income', 0.0):.2f}
- Total expense: ₹{summary.get('total_expense', 0.0):.2f}
- Balance: ₹{summary.get('balance', 0.0):.2f}
- Average income transaction: ₹{summary.get('average_income', 0.0):.2f}
- Average expense transaction: ₹{summary.get('average_expense', 0.0):.2f}
- Top spending category: {summary.get('top_category', 'N/A')}

Category breakdown:
{category_lines}

Generated insights:
{insight_lines}

Explain the user's financial situation in simple, factual language.
Do not invent numbers.
Keep the response concise.

Give:
1. A short summary
2. Two risks
3. Three practical suggestions
4. One budgeting tip
""".strip()

    return prompt