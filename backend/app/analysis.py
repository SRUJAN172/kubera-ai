from __future__ import annotations

from typing import Any, Dict
import pandas as pd


VALID_TYPES = {"income", "expense"}
OUTLIER_LIMIT = 100000
OVERSPENDING_THRESHOLD = 0.30
EXPENSE_RATIO_HIGH = 80
EXPENSE_RATIO_MODERATE = 60


class FinancialAnalyzer:
    REQUIRED_COLUMNS = {"date", "type", "amount"}

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self._prepare_data()

    def _prepare_data(self) -> None:
        self.df.columns = self.df.columns.str.strip().str.lower()

        missing = self.REQUIRED_COLUMNS - set(self.df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

        self.df["date"] = pd.to_datetime(self.df["date"], errors="coerce")
        self.df["amount"] = pd.to_numeric(self.df["amount"], errors="coerce")
        self.df["type"] = self.df["type"].astype(str).str.strip().str.lower()

        if "category" in self.df.columns:
            self.df["category"] = (
                self.df["category"]
                .astype(str)
                .str.strip()
                .str.lower()
                .replace("", "unknown")
                .fillna("unknown")
            )
        else:
            self.df["category"] = "unknown"

        if "description" in self.df.columns:
            self.df["description"] = self.df["description"].fillna("").astype(str).str.strip()
        else:
            self.df["description"] = ""

        self.df = self.df.dropna(subset=["amount", "type"])
        self.df = self.df[self.df["type"].isin(VALID_TYPES)]
        self.df = self.df[self.df["amount"] > 0]
        self.df = self.df[self.df["amount"] < OUTLIER_LIMIT]

    def _income_df(self) -> pd.DataFrame:
        return self.df[self.df["type"] == "income"]

    def _expense_df(self) -> pd.DataFrame:
        return self.df[self.df["type"] == "expense"]

    def _monthly_sum(self, frame: pd.DataFrame) -> Dict[str, float]:
        if frame.empty or frame["date"].isna().all():
            return {}

        trend = (
            frame.dropna(subset=["date"])
            .groupby(frame.dropna(subset=["date"])["date"].dt.to_period("M"))["amount"]
            .sum()
            .sort_index()
        )
        return {str(month): float(amount) for month, amount in trend.items()}

    def transaction_count(self) -> int:
        return int(len(self.df))

    def income_count(self) -> int:
        return int(len(self._income_df()))

    def expense_count(self) -> int:
        return int(len(self._expense_df()))

    def total_income(self) -> float:
        return float(self._income_df()["amount"].sum())

    def total_expense(self) -> float:
        return float(self._expense_df()["amount"].sum())

    def savings(self) -> float:
        return float(self.total_income() - self.total_expense())

    def net_cash_flow(self) -> float:
        return self.savings()

    def savings_rate(self) -> float:
        income = self.total_income()
        if income == 0:
            return 0.0
        rate = (self.savings() / income) * 100
        return round(max(min(rate, 100), -100), 2)

    def expense_ratio(self) -> float:
        income = self.total_income()
        if income == 0:
            return 0.0
        ratio = (self.total_expense() / income) * 100
        return round(min(ratio, 100), 2)

    def category_spending(self) -> Dict[str, float]:
        expenses = self._expense_df()
        if expenses.empty:
            return {}

        grouped = (
            expenses.groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )
        return {category: float(amount) for category, amount in grouped.items()}

    def top_3_expense_categories(self) -> list[Dict[str, float | str]]:
        categories = self.category_spending()
        top_items = list(categories.items())[:3]
        return [
            {"category": category, "amount": float(amount)}
            for category, amount in top_items
        ]

    def monthly_income_trend(self) -> Dict[str, float]:
        return self._monthly_sum(self._income_df())

    def monthly_expense_trend(self) -> Dict[str, float]:
        return self._monthly_sum(self._expense_df())

    def monthly_savings_trend(self) -> Dict[str, float]:
        income_trend = self.monthly_income_trend()
        expense_trend = self.monthly_expense_trend()

        all_months = sorted(set(income_trend) | set(expense_trend))
        return {
            month: float(income_trend.get(month, 0.0) - expense_trend.get(month, 0.0))
            for month in all_months
        }

    def highest_expense(self) -> Dict[str, Any]:
        expenses = self._expense_df()
        if expenses.empty:
            return {}

        highest = expenses.nlargest(1, "amount").iloc[0]
        return {
            "date": str(highest["date"].date()) if pd.notna(highest["date"]) else None,
            "category": highest.get("category", "unknown"),
            "amount": float(highest["amount"]),
            "description": highest.get("description", ""),
        }

    def highest_spending_day(self) -> Dict[str, float | str]:
        expenses = self._expense_df().dropna(subset=["date"])
        if expenses.empty:
            return {}

        daily = expenses.groupby(expenses["date"].dt.date)["amount"].sum()
        highest = daily.nlargest(1)

        return {
            "date": str(highest.index[0]),
            "amount": float(highest.iloc[0]),
        }

    def average_monthly_spending(self) -> float:
        expense_trend = self.monthly_expense_trend()
        if not expense_trend:
            return 0.0
        return round(sum(expense_trend.values()) / len(expense_trend), 2)

    def average_expense_per_transaction(self) -> float:
        expenses = self._expense_df()
        if expenses.empty:
            return 0.0
        return round(float(expenses["amount"].mean()), 2)

    def overspending_categories(self, threshold: float = OVERSPENDING_THRESHOLD) -> Dict[str, float]:
        total = self.total_expense()
        categories = self.category_spending()

        if total == 0:
            return {}

        return {
            category: amount
            for category, amount in categories.items()
            if (amount / total) > threshold
        }

    def expense_alert(self) -> str:
        ratio = self.expense_ratio()
        if ratio > EXPENSE_RATIO_HIGH:
            return "High spending! Reduce expenses."
        if ratio > EXPENSE_RATIO_MODERATE:
            return "Moderate spending."
        return "Good control over expenses."

    def budget_warning(self) -> Dict[str, str]:
        ratio = self.expense_ratio()
        savings = self.savings()

        if savings < 0:
            return {
                "status": "danger",
                "message": "You are overspending. Your expenses are greater than your income.",
            }
        if ratio >= 90:
            return {
                "status": "warning",
                "message": "Your expenses are very high compared to your income.",
            }
        if ratio >= 75:
            return {
                "status": "caution",
                "message": "Your spending is getting close to your income. Track it carefully.",
            }
        return {
            "status": "healthy",
            "message": "Your budget is under control.",
        }

    def financial_health(self) -> str:
        rate = self.savings_rate()
        if rate >= 30:
            return "Excellent"
        if rate >= 15:
            return "Good"
        if rate >= 5:
            return "Average"
        return "Poor"

    def full_analysis(self) -> Dict[str, Any]:
        return {
            "total_transactions": self.transaction_count(),
            "income_transactions": self.income_count(),
            "expense_transactions": self.expense_count(),
            "total_income": self.total_income(),
            "total_expense": self.total_expense(),
            "savings": self.savings(),
            "net_cash_flow": self.net_cash_flow(),
            "savings_rate": self.savings_rate(),
            "expense_ratio": self.expense_ratio(),
            "category_spending": self.category_spending(),
            "top_3_expense_categories": self.top_3_expense_categories(),
            "highest_expense": self.highest_expense(),
            "highest_spending_day": self.highest_spending_day(),
            "monthly_income_trend": self.monthly_income_trend(),
            "monthly_expense_trend": self.monthly_expense_trend(),
            "monthly_savings_trend": self.monthly_savings_trend(),
            "average_monthly_spending": self.average_monthly_spending(),
            "average_expense_per_transaction": self.average_expense_per_transaction(),
            "overspending_categories": self.overspending_categories(),
            "expense_alert": self.expense_alert(),
            "budget_warning": self.budget_warning(),
            "financial_health": self.financial_health(),
        }


def load_transactions(csv_path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(csv_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    except Exception as e:
        raise Exception(f"Error reading CSV file: {e}")