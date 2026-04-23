from __future__ import annotations

from typing import Any, Dict, List


SAVINGS_RATE_WARNING = 20
HIGH_CATEGORY_PERCENT = 30
EXPENSE_RATIO_WARNING = 80
EXPENSE_RATIO_MODERATE = 60


def _format_currency(value: float) -> str:
    return f"₹{value:.2f}"


def _build_category_lines(category_spending: Dict[str, float]) -> str:
    if not category_spending:
        return "- No category spending data available"

    return "\n".join(
        f"- {category}: {_format_currency(amount)}"
        for category, amount in category_spending.items()
    )


def _build_trend_lines(
    income_trend: Dict[str, float],
    expense_trend: Dict[str, float],
    savings_trend: Dict[str, float],
) -> str:
    all_months = sorted(set(income_trend) | set(expense_trend) | set(savings_trend))
    if not all_months:
        return "- No monthly trend data available"

    return "\n".join(
        (
            f"- {month}: "
            f"Income {_format_currency(income_trend.get(month, 0.0))}, "
            f"Expense {_format_currency(expense_trend.get(month, 0.0))}, "
            f"Savings {_format_currency(savings_trend.get(month, 0.0))}"
        )
        for month in all_months
    )


def _build_insight_lines(insights: List[str]) -> str:
    if not insights:
        return "- No insights generated"
    return "\n".join(f"- {insight}" for insight in insights)


def generate_insights(summary: Dict[str, Any]) -> List[str]:
    """Generate human-readable insights from financial summary data."""
    insights: List[str] = []

    total_transactions = int(summary.get("total_transactions", 0))
    income_transactions = int(summary.get("income_transactions", 0))
    expense_transactions = int(summary.get("expense_transactions", 0))

    total_income = float(summary.get("total_income", 0.0))
    total_expense = float(summary.get("total_expense", 0.0))
    savings = float(summary.get("savings", 0.0))
    savings_rate = float(summary.get("savings_rate", 0.0))
    expense_ratio = float(summary.get("expense_ratio", 0.0))
    net_cash_flow = float(summary.get("net_cash_flow", 0.0))
    average_monthly_spending = float(summary.get("average_monthly_spending", 0.0))
    average_expense_per_transaction = float(
        summary.get("average_expense_per_transaction", 0.0)
    )

    category_spending = summary.get("category_spending", {}) or {}
    top_categories = summary.get("top_3_expense_categories", []) or []
    highest_expense = summary.get("highest_expense", {}) or {}
    highest_spending_day = summary.get("highest_spending_day", {}) or {}
    overspending_categories = summary.get("overspending_categories", {}) or {}
    budget_warning = summary.get("budget_warning", {}) or {}
    expense_alert = summary.get("expense_alert", "")
    financial_health = summary.get("financial_health", "Unknown")

    if total_transactions == 0:
        return ["No transactions were found. Upload more data to generate insights."]

    insights.append(
        f"You recorded {total_transactions} transactions, including "
        f"{income_transactions} income entries and {expense_transactions} expense entries."
    )

    if total_income == 0:
        insights.append(
            "No income was recorded. Savings and expense analysis may be incomplete."
        )
    else:
        insights.append(f"Your total income is {_format_currency(total_income)}.")
        insights.append(f"Your total expense is {_format_currency(total_expense)}.")
        insights.append(f"Your current savings are {_format_currency(savings)}.")
        insights.append(f"Your savings rate is {savings_rate:.2f}%.")

    if savings < 0:
        insights.append(
            f"You are overspending and currently running a deficit of {_format_currency(abs(savings))}."
        )
    elif savings == 0:
        insights.append("Your income and expenses are balanced with no savings left.")
    else:
        insights.append("You are spending less than you earn, which is a healthy sign.")

    if savings_rate < SAVINGS_RATE_WARNING:
        insights.append(
            "Your savings rate is below 20%. Consider reducing non-essential expenses."
        )
    else:
        insights.append("Your savings rate looks healthy.")

    insights.append(f"Your expense ratio is {expense_ratio:.2f}% of your income.")

    if expense_ratio > EXPENSE_RATIO_WARNING:
        insights.append(
            "A very large portion of your income is going toward expenses. This needs attention."
        )
    elif expense_ratio > EXPENSE_RATIO_MODERATE:
        insights.append("Your expenses are moderately high compared to your income.")
    else:
        insights.append("Your expenses appear to be under reasonable control.")

    if top_categories:
        top = top_categories[0]
        insights.append(
            f"Your highest spending category is '{top.get('category', 'unknown')}' "
            f"with {_format_currency(float(top.get('amount', 0.0)))} spent."
        )

        top_text = ", ".join(
            f"{item.get('category', 'unknown')} ({_format_currency(float(item.get('amount', 0.0)))})"
            for item in top_categories
        )
        insights.append(f"Top expense categories: {top_text}.")

    if total_expense > 0 and category_spending:
        for category, amount in category_spending.items():
            percent = (float(amount) / total_expense) * 100
            if percent >= HIGH_CATEGORY_PERCENT:
                insights.append(
                    f"'{category}' accounts for {percent:.2f}% of your total expenses, which is quite high."
                )

    if highest_expense:
        insights.append(
            f"Your highest single expense was in '{highest_expense.get('category', 'unknown')}' "
            f"for {_format_currency(float(highest_expense.get('amount', 0.0)))}."
        )

    if highest_spending_day:
        insights.append(
            f"Your highest spending day was {highest_spending_day.get('date', 'N/A')} "
            f"with total spending of {_format_currency(float(highest_spending_day.get('amount', 0.0)))}."
        )

    if average_monthly_spending > 0:
        insights.append(
            f"Your average monthly spending is approximately {_format_currency(average_monthly_spending)}."
        )

    if average_expense_per_transaction > 0:
        insights.append(
            f"Your average expense per transaction is {_format_currency(average_expense_per_transaction)}."
        )

    if overspending_categories:
        overspending_text = ", ".join(
            f"{category} ({_format_currency(float(amount))})"
            for category, amount in overspending_categories.items()
        )
        insights.append(
            f"These categories are taking a large share of your expenses: {overspending_text}."
        )

    if budget_warning:
        message = budget_warning.get("message")
        if message:
            insights.append(message)

    if expense_alert:
        insights.append(expense_alert)

    insights.append(f"Overall financial health: {financial_health}.")

    if net_cash_flow > 0:
        insights.append("Your net cash flow is positive.")
    elif net_cash_flow < 0:
        insights.append("Your net cash flow is negative.")
    else:
        insights.append("Your net cash flow is neutral.")

    return insights


def build_ai_prompt(summary: Dict[str, Any], insights: List[str]) -> str:
    """Prepare a structured prompt for an LLM using the current analysis structure."""
    category_spending = summary.get("category_spending", {}) or {}
    highest_expense = summary.get("highest_expense", {}) or {}
    highest_spending_day = summary.get("highest_spending_day", {}) or {}

    income_trend = summary.get("monthly_income_trend", {}) or {}
    expense_trend = summary.get("monthly_expense_trend", {}) or {}
    savings_trend = summary.get("monthly_savings_trend", {}) or {}

    category_lines = _build_category_lines(category_spending)
    trend_lines = _build_trend_lines(income_trend, expense_trend, savings_trend)
    insight_lines = _build_insight_lines(insights)

    prompt = f"""
You are Kubera AI, a personal finance assistant.

Here is the financial summary:
- Total transactions: {summary.get('total_transactions', 0)}
- Income transactions: {summary.get('income_transactions', 0)}
- Expense transactions: {summary.get('expense_transactions', 0)}
- Total income: {_format_currency(float(summary.get('total_income', 0.0)))}
- Total expense: {_format_currency(float(summary.get('total_expense', 0.0)))}
- Savings: {_format_currency(float(summary.get('savings', 0.0)))}
- Savings rate: {float(summary.get('savings_rate', 0.0)):.2f}%
- Expense ratio: {float(summary.get('expense_ratio', 0.0)):.2f}%
- Financial health: {summary.get('financial_health', 'Unknown')}
- Net cash flow: {_format_currency(float(summary.get('net_cash_flow', 0.0)))}
- Average monthly spending: {_format_currency(float(summary.get('average_monthly_spending', 0.0)))}
- Average expense per transaction: {_format_currency(float(summary.get('average_expense_per_transaction', 0.0)))}
- Expense alert: {summary.get('expense_alert', 'N/A')}
- Budget warning: {summary.get('budget_warning', {}).get('message', 'N/A')}

Highest expense:
- Category: {highest_expense.get('category', 'N/A')}
- Amount: {_format_currency(float(highest_expense.get('amount', 0.0)))}
- Date: {highest_expense.get('date', 'N/A')}
- Description: {highest_expense.get('description', 'N/A')}

Highest spending day:
- Date: {highest_spending_day.get('date', 'N/A')}
- Amount: {_format_currency(float(highest_spending_day.get('amount', 0.0)))}

Category spending:
{category_lines}

Monthly trends:
{trend_lines}

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