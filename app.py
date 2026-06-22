from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from service import ask_ai

from analytics import (
    dashboard_data,
    get_kpis,
    sales_by_region,
    sales_by_category,
    top_products,
    monthly_sales,
    payment_methods,
    gender_sales,
    age_group_sales
)

# ==========================================
# FastAPI App
# ==========================================

app = FastAPI(title="AI Power BI Assistant")

# ==========================================
# Request Model
# ==========================================

class ChatRequest(BaseModel):
    question: str

# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# Static Files & Templates
# ==========================================

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# ==========================================
# Home Page
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

# ==========================================
# Chat Endpoint
# ==========================================

@app.post("/chat")
async def chat(payload: ChatRequest):

    question = payload.question.strip()

    if question == "":
        return {
            "success": False,
            "answer": "Please enter a question."
        }

    try:

        answer = ask_ai(question)

        return {
            "success": True,
            "question": question,
            "answer": answer
        }

    except Exception as e:

        print(e)

        return {
            "success": False,
            "answer": str(e)
        }

# ==========================================
# Health Check
# ==========================================

@app.get("/health")
async def health():

    return {
        "status": "running",
        "service": "AI Power BI Assistant"
    }

# ==========================================
# Dashboard
# ==========================================

@app.get("/dashboard")
async def dashboard():

    return dashboard_data()

# ==========================================
# KPI
# ==========================================

@app.get("/kpis")
async def kpis():

    return get_kpis()

# ==========================================
# Charts
# ==========================================

@app.get("/charts/region")
async def chart_region():

    return sales_by_region()


@app.get("/charts/category")
async def chart_category():

    return sales_by_category()


@app.get("/charts/products")
async def chart_products():

    return top_products()


@app.get("/charts/monthly")
async def chart_monthly():

    return monthly_sales()


@app.get("/charts/payment")
async def chart_payment():

    return payment_methods()


@app.get("/charts/gender")
async def chart_gender():

    return gender_sales()


@app.get("/charts/age")
async def chart_age():

    return age_group_sales()