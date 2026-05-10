from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
import pandas as pd
import tempfile

from database import Base, engine, SessionLocal
from models import User, Transaction
from analysis import load_transactions, FinancialAnalyzer
from insights import generate_insights, build_ai_prompt
from llm_service import generate_explanation
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)

# ------------------ APP SETUP ------------------

app = FastAPI(title="Kubera AI")
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------ DB DEPENDENCY ------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------ PER-USER CACHE ------------------

_user_cache: dict[int, FinancialAnalyzer] = {}


def get_cached_data(user_id: int) -> FinancialAnalyzer:
    if user_id not in _user_cache:
        df = load_transactions(engine, user_id)
        _user_cache[user_id] = FinancialAnalyzer(df)
    return _user_cache[user_id]


def clear_user_cache(user_id: int):
    _user_cache.pop(user_id, None)


def get_pipeline_data(user_id: int):
    analyzer = get_cached_data(user_id)
    summary = analyzer.full_analysis()
    insights = generate_insights(summary)
    prompt = build_ai_prompt(summary, insights)
    return analyzer, summary, insights, prompt


# ------------------ AUTH SCHEMAS ------------------

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


# ------------------ AUTH ROUTES ------------------

@app.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=req.name,
        email=req.email,
        hashed_password=hash_password(req.password),
        created_at=str(datetime.utcnow().date()),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.email})
    return {
        "status": "success",
        "token": token,
        "user": {"id": user.id, "name": user.name, "email": user.email},
    }


@app.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()

    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user.email})
    return {
        "status": "success",
        "token": token,
        "user": {"id": user.id, "name": user.name, "email": user.email},
    }


@app.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "status": "success",
        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
        },
    }


# ------------------ ROUTES ------------------

from sqlalchemy import text

@app.get("/")
def home():
    return {"message": "Kubera AI backend is running"}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Try to execute a simple query to check DB connection
        db.execute(text("SELECT 1"))
        return {"status": "success", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "error": str(e)}


@app.get("/analyze")
def analyze(current_user: User = Depends(get_current_user)):
    try:
        _, summary, _, _ = get_pipeline_data(current_user.id)
        return {"status": "success", "data": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/insights")
def insights_route(current_user: User = Depends(get_current_user)):
    try:
        _, summary, insights, _ = get_pipeline_data(current_user.id)
        return {"status": "success", "summary": summary, "insights": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/prompt")
def prompt_route(current_user: User = Depends(get_current_user)):
    try:
        _, summary, insights, prompt = get_pipeline_data(current_user.id)
        return {
            "status": "success",
            "summary": summary,
            "insights": insights,
            "prompt": prompt,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/explain")
def explain_route(current_user: User = Depends(get_current_user)):
    try:
        _, summary, insights, prompt = get_pipeline_data(current_user.id)
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
def ask(data: dict, current_user: User = Depends(get_current_user)):
    try:
        query = data.get("query", "")

        if not query.strip():
            raise HTTPException(status_code=400, detail="Query is required")

        history = data.get("history", [])

        _, summary, insights, _ = get_pipeline_data(current_user.id)

        history_text = "\n".join(
            [
                f"{msg.get('role', 'user')}: {msg.get('content', '')}"
                for msg in history[-5:]
            ]
        )

        explanation_prompt = f"""
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
            - Explain the user's financial situation clearly
            - Use only the data above
            - Be concise
            - Do not hallucinate
            """

        advice_prompt = f"""
            You are Kubera AI, a personal finance advisor.

            Based on the user's financial data, give ONLY actionable advice.

            Financial Summary:
            - Total Income: ₹{summary['total_income']}
            - Total Expense: ₹{summary['total_expense']}
            - Savings: ₹{summary['savings']}
            - Savings Rate: {summary['savings_rate']}%
            - Expense Ratio: {summary['expense_ratio']}%
            - Financial Health: {summary['financial_health']}

            Top Expense Categories:
            {summary['top_3_expense_categories']}

            Insights:
            {insights}

            User Question:
            {query}

            Rules:
            - Do not repeat the full explanation
            - Give 3 to 5 practical points
            - Focus on improving savings and reducing unnecessary expenses
            - Be concise
            - Do not hallucinate
            - Avoid risky investment advice

            Format:
            - Advice 1
            - Advice 2
            - Advice 3
            """

        explanation = generate_explanation(explanation_prompt)
        advice = generate_explanation(advice_prompt)

        return {
            "status": "success",
            "query": query,
            "answer": {
                "explanation": explanation,
                "advice": advice,
            },
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------ GOALS ------------------

@app.get("/goals")
def get_goals(current_user: User = Depends(get_current_user)):
    try:
        _, summary, _, _ = get_pipeline_data(current_user.id)

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


# ------------------ TRANSACTIONS ------------------

@app.get("/transactions")
def get_transactions(current_user: User = Depends(get_current_user)):
    try:
        analyzer = get_cached_data(current_user.id)
        df = analyzer.df.copy()

        if "date" in df.columns:
            df["date"] = df["date"].astype(str)

        records = df.to_dict(orient="records")

        return {
            "status": "success",
            "count": len(records),
            "data": records,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/transactions/export")
def export_transactions(current_user: User = Depends(get_current_user)):
    try:
        analyzer = get_cached_data(current_user.id)
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


@app.get("/subscriptions")
def get_subscriptions(current_user: User = Depends(get_current_user)):
    try:
        analyzer = get_cached_data(current_user.id)
        subs = analyzer.detect_subscriptions()
        
        total_monthly_cost = sum(sub["amount"] for sub in subs)
        
        return {
            "status": "success",
            "total_monthly_cost": total_monthly_cost,
            "subscriptions": subs
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------ UPLOAD ------------------

@app.post("/upload")
async def upload_csv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        if not file.filename.lower().endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files allowed")

        df = pd.read_csv(file.file)
        df.columns = df.columns.str.strip().str.lower()

        required_cols = {"date", "type", "category", "amount"}

        if not required_cols.issubset(df.columns):
            missing = required_cols - set(df.columns)
            raise HTTPException(
                status_code=400,
                detail=f"Missing columns: {missing}",
            )

        if "description" not in df.columns:
            df["description"] = ""

        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        df["type"] = (
            df["type"]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.lower()
        )

        df["category"] = (
            df["category"]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
            .replace("", "Unknown")
        )

        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

        df["description"] = (
            df["description"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        inserted = 0
        skipped = 0
        skipped_invalid = 0
        skipped_duplicate = 0

        for _, row in df.iterrows():
            if pd.isna(row["date"]) or row["type"] not in ["income", "expense"]:
                skipped += 1
                skipped_invalid += 1
                continue

            date_value = str(row["date"].date())
            type_value = row["type"]
            category_value = row["category"]
            amount_value = float(row["amount"])
            description_value = row["description"]

            exists = db.query(Transaction).filter(
                Transaction.user_id == current_user.id,
                Transaction.date == date_value,
                Transaction.type == type_value,
                Transaction.category == category_value,
                Transaction.amount == amount_value,
                Transaction.description == description_value,
            ).first()

            if exists:
                skipped += 1
                skipped_duplicate += 1
                continue

            transaction = Transaction(
                user_id=current_user.id,
                date=date_value,
                type=type_value,
                category=category_value,
                amount=amount_value,
                description=description_value,
            )

            db.add(transaction)
            inserted += 1

        db.commit()
        clear_user_cache(current_user.id)

        return {
            "status": "success",
            "message": "CSV uploaded successfully",
            "total_rows": len(df),
            "inserted": inserted,
            "rows": inserted,
            "skipped": skipped,
            "skipped_invalid": skipped_invalid,
            "skipped_duplicate": skipped_duplicate,
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        print("UPLOAD ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload-receipt")
async def upload_receipt(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        import base64
        from llm_service import analyze_receipt
        
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Only image files are allowed.")
            
        file_bytes = await file.read()
        b64_image = base64.b64encode(file_bytes).decode('utf-8')
        
        # Call the Vision AI
        receipt_data = analyze_receipt(b64_image, file.content_type)
        
        # The AI should return amount, description, date, category
        date_str = receipt_data.get("date", str(datetime.utcnow().date()))
        amount = float(receipt_data.get("amount", 0.0))
        description = receipt_data.get("description", "Unknown Merchant")
        category = receipt_data.get("category", "Others")
        
        transaction = Transaction(
            user_id=current_user.id,
            date=date_str,
            type="expense",
            category=category,
            amount=amount,
            description=description,
        )
        
        db.add(transaction)
        db.commit()
        clear_user_cache(current_user.id)
        
        return {
            "status": "success",
            "message": "Receipt processed successfully",
            "data": receipt_data
        }
        
    except Exception as e:
        db.rollback()
        print("RECEIPT UPLOAD ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))


# ------------------ DELETE & CACHE ------------------

@app.delete("/delete")
def delete_all_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        deleted = db.query(Transaction).filter(
            Transaction.user_id == current_user.id,
        ).delete()
        db.commit()
        clear_user_cache(current_user.id)

        return {
            "status": "success",
            "message": "All transactions deleted",
            "rows_deleted": deleted,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/refresh")
def refresh_cache(current_user: User = Depends(get_current_user)):
    clear_user_cache(current_user.id)
    return {"status": "success", "message": "Cache refreshed"}
