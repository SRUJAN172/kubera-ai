from fastapi import FastAPI, HTTPException
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from analysis import load_transactions, analyze_transactions
from insights import generate_insights, build_ai_prompt
from llm_service import generate_explanation

app = FastAPI()

#the CORSMiddleware which helps to  link the frontend and backend , it makes the resource access possible to run b/w the local system
#Cross-Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "sample_transactions.csv"


def get_pipeline_data():
    df = load_transactions(CSV_PATH)
    summary = analyze_transactions(df)
    insights = generate_insights(summary)
    prompt = build_ai_prompt(summary, insights)
    return summary, insights, prompt


@app.get("/")
def home():
    return {"message": "Kubera AI backend is running"}


@app.get("/analyze")
def analyze():
    summary, _, _ = get_pipeline_data()
    return summary


@app.get("/insights")
def insights_route():
    summary, insights, _ = get_pipeline_data()
    return {
        "summary": summary,
        "insights": insights
    }


@app.get("/prompt")
def prompt_route():
    summary, insights, prompt = get_pipeline_data()
    return {
        "summary": summary,
        "insights": insights,
        "prompt": prompt
    }


@app.get("/explain")
def explain_route():
    try:
        summary, insights, prompt = get_pipeline_data()
        explanation = generate_explanation(prompt)

        return {
            "summary": summary,
            "insights": insights,
            "explanation": explanation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ask")
def ask(query:str):
    data = load_transactions(CSV_PATH)
    summary = analyze_transactions(data)
    prompt = f"""
    you are a finiancial assistant

    Rules:
    -Answer clearly
    -Use numbers when possible
    -Be concise

    Data:{data}

    Question:{query}
    """
    response = generate_explanation(prompt)
    return {"answer":response}

