from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

import pandas as pd


def load_transactions(csv_path: str | Path) -> pd.DataFrame:
    """Load and validate transaction data from a CSV file."""
    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    df = pd.read_csv(path)

    required_columns = {"date", "description", "amount", "type", "category"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["type"] = df["type"].astype(str).str.strip().str.lower()
    df["category"] = df["category"].astype(str).str.strip().str.lower()

    if df["date"].isna().any():
        raise ValueError("Some dates are invalid in the CSV.")

    if df["amount"].isna().any():
        raise ValueError("Some amounts are invalid in the CSV.")

    valid_types = {"income", "expense"}
    invalid_types = set(df["type"]) - valid_types
    if invalid_types:
        raise ValueError(f"Invalid transaction types found: {sorted(invalid_types)}")

    return df


def analyze_transactions(df: pd.DataFrame) -> Dict[str, Any]:
    """Generate summary statistics from transaction data."""
    income_df = df[df["type"] == "income"]
    expense_df = df[df["type"] == "expense"]

    total_income = float(income_df["amount"].sum())
    total_expense = float(expense_df["amount"].sum())
    balance = total_income - total_expense

    category_spending = (
        expense_df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    top_category = category_spending.index[0] if not category_spending.empty else None
    top_category_amount = float(category_spending.iloc[0]) if not category_spending.empty else 0.0

    transaction_count = len(df)
    expense_count = len(expense_df)
    income_count = len(income_df)

    average_expense = float(expense_df["amount"].mean()) if not expense_df.empty else 0.0
    average_income = float(income_df["amount"].mean()) if not income_df.empty else 0.0

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "transaction_count": transaction_count,
        "income_count": income_count,
        "expense_count": expense_count,
        "average_income": average_income,
        "average_expense": average_expense,
        "top_category": top_category,
        "top_category_amount": top_category_amount,
        "category_breakdown": category_spending.to_dict(),
    }