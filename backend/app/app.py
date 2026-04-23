from fastapi import FastAPI, HTTPException
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from analysis import load_transactions, FinancialAnalyzer
from insights import generate_insights, build_ai_prompt
from llm_service import generate_explanation
from functools import lru_cache
import tempfile

app = FastAPI()

# ------------------ CORS ------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "sample_transactions.csv"


# ------------------ CACHE ------------------
@lru_cache(maxsize=1)
def get_cached_data():
    df = load_transactions(CSV_PATH)
    return FinancialAnalyzer(df)


def get_pipeline_data():
    analyzer = get_cached_data()
    summary = analyzer.full_analysis()
    insights = generate_insights(summary)
    prompt = build_ai_prompt(summary, insights)
    return analyzer, summary, insights, prompt


# ------------------ ROUTES ------------------

@app.get("/")
def home():
    return {"message": "Kubera AI backend is running"}


@app.get("/analyze")
def analyze():
    try:
        _, summary, _, _ = get_pipeline_data()
        return {"status": "success", "data": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/insights")
def insights_route():
    try:
        _, summary, insights, _ = get_pipeline_data()
        return {"status": "success", "summary": summary, "insights": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/prompt")
def prompt_route():
    try:
        _, summary, insights, prompt = get_pipeline_data()
        return {
            "status": "success",
            "summary": summary,
            "insights": insights,
            "prompt": prompt,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/explain")
def explain_route():
    try:
        _, summary, insights, prompt = get_pipeline_data()
        explanation = generate_explanation(prompt)

        return {
            "status": "success",
            "summary": summary,
            "insights": insights,
            "explanation": explanation,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------ ASK (AI CHAT) ------------------

@app.post("/ask")
def ask(data: dict):
    try:
        query = data.get("query", "")
        if not query.strip():
            raise HTTPException(status_code=400, detail="Query is required")

        history = data.get("history", [])

        _, summary, insights, _ = get_pipeline_data()

        history_text = "\n".join(
            [f"{msg.get('role', 'user')}: {msg.get('content', '')}" for msg in history[-5:]]
        )

        prompt = f"""
You are Kubera AI, a personal finance assistant.

Financial Summary:
- Total Income: ₹{summary['total_income']}
- Total Expense: ₹{summary['total_expense']}
- Savings: ₹{summary['savings']}
- Savings Rate: {summary['savings_rate']}%
- Expense Ratio: {summary['expense_ratio']}%
- Financial Health: {summary['financial_health']}

Top Expense Categories:
{summary['top_3_expense_categories']}

Monthly Trends:
Income: {summary['monthly_income_trend']}
Expense: {summary['monthly_expense_trend']}
Savings: {summary['monthly_savings_trend']}

Insights:
{insights}

Conversation History:
{history_text}

User Question:
{query}

Rules:
- Use the data above
- Be concise
- Give actionable advice
- Do not hallucinate
"""

        response = generate_explanation(prompt)

        return {
            "status": "success",
            "query": query,
            "answer": response,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------ GOALS ------------------

@app.get("/goals")
def get_goals():
    try:
        _, summary, _, _ = get_pipeline_data()

        emergency_target = summary["total_expense"] * 6

        progress = 0
        if emergency_target > 0:
            progress = min((summary["savings"] / emergency_target) * 100, 100)

        goals = [
            {
                "title": "Emergency Fund",
                "value": round(max(progress, 0), 2),
                "amount": f"₹{summary['savings']:.0f} / ₹{emergency_target:.0f}",
            },
            {
                "title": "Savings Goal",
                "value": summary["savings_rate"],
                "amount": f"{summary['savings_rate']}%",
            },
            {
                "title": "Expense Control",
                "value": max(100 - summary["expense_ratio"], 0),
                "amount": f"{summary['expense_ratio']}% used",
            },
        ]

        return {"status": "success", "data": goals}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# ------------------ EXPORT ------------------

@app.get("/transactions/export")
def export_transactions():
    try:
        analyzer = get_cached_data()
        df = analyzer.df.copy()

        if "date" in df.columns:
            df["date"] = df["date"].astype(str)

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        df.to_csv(temp_file.name, index=False)

        return FileResponse(
            path=temp_file.name,
            media_type="text/csv",
            filename="kubera_transactions.csv",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/transactions")
def get_transactions():
    try:
        analyzer = get_cached_data()
        df = analyzer.df.copy()

        if "date" in df.columns:
            df["date"] = df["date"].astype(str)

        records = df.to_dict(orient="records")

        return {
            "status": "success",
            "count": len(records),
            "data": records
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# ------------------ CACHE REFRESH ------------------

@app.post("/refresh")
def refresh_cache():
    get_cached_data.cache_clear()
    return {"status": "success", "message": "Cache refreshed"}