from groq import Groq
from dotenv import load_dotenv
from memory import memory
import os
import re


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------------------------------
# Available Functions
# ---------------------------------------

AVAILABLE_FUNCTIONS = [
    "highest_selling_product",
    "lowest_selling_product",
    "top_products",

    "highest_region_sales",
    "region_sales",

    "men_vs_women",

    "sales_by_payment",
    "sales_by_category",
    "sales_by_age_group",

    "top_payment_method",
    "top_age_group",
    "best_category",
    "most_profitable_product",
    "sales_growth",

    "total_sales",
    "total_profit",
    "total_orders",
    "average_order_value",

    "dashboard_summary"
]

# ---------------------------------------
# Local Intent Dictionary
# ---------------------------------------

LOCAL_INTENTS = {

    "highest_selling_product": [
        "highest selling product",
        "best selling product",
        "best seller",
        "top product",
        "top selling",
        "most sold",
        "most popular product",
        "highest quantity",
        "maximum sales product",
        "which product sold the most"
    ],

    "lowest_selling_product": [
        "lowest selling product",
        "least selling product",
        "worst selling",
        "least sold",
        "lowest quantity"
    ],

    "top_products": [
        "top products",
        "top 5 products",
        "best products",
        "popular products"
    ],

    "highest_region_sales": [
        "highest region",
        "best region",
        "top region",
        "highest sales region",
        "highest revenue",
        "which region has highest sales"
    ],

    "region_sales": [
        "sales by region",
        "region wise sales",
        "show regions",
        "all region sales"
    ],

    "men_vs_women": [
        "men vs women",
        "male vs female",
        "gender",
        "customer gender",
        "compare men",
        "compare women"
    ],

    "sales_by_payment": [
        "payment method",
        "payment",
        "payment wise",
        "payment analysis"
    ],

    "sales_by_category": [
        "category sales",
        "sales by category",
        "product category",
        "category analysis"
    ],

    "sales_by_age_group": [
        "age group",
        "sales by age",
        "age analysis"
    ],

    "total_sales": [
        "total sales",
        "overall sales",
        "sales revenue",
        "revenue"
    ],

    "total_profit": [
        "profit",
        "profits",
        "total profit",
        "overall profit",
        "net profit",
        "profit made",
        "earnings"
    ],

    "total_orders": [
        "orders",
        "total orders",
        "number of orders",
        "how many orders"
    ],

    "average_order_value": [
        "average order",
        "average order value",
        "average sale"
    ],

    "top_payment_method": [
        "top payment method",
        "best payment method",
        "most used payment",
        "preferred payment",
        "payment method used most"
    ],

    "top_age_group": [
        "top age group",
        "best age group",
        "highest age group sales",
        "which age group buys the most",
        "most active age group"
    ],

    "best_category": [
        "best category",
        "top category",
        "highest selling category",
        "most profitable category",
        "category performance"
    ],

    "most_profitable_product": [
        "most profitable product",
        "highest profit product",
        "best profit product",
        "top profit product"
    ],

    "sales_growth": [
        "sales growth",
        "growth rate",
        "month over month growth",
        "monthly growth",
        "sales trend"
    ],

    "dashboard_summary": [
        "dashboard",
        "summary",
        "overview",
        "business summary",
        "report"
    ]
}


# ---------------------------------------
# Normalize
# ---------------------------------------

def normalize(question):

    return (
        question.lower()
        .replace("?", "")
        .replace(",", "")
        .replace(".", "")
        .strip()
    )


# ---------------------------------------
# Follow-up Detection
# ---------------------------------------

FOLLOW_UP_WORDS = [
    "it",
    "that",
    "those",
    "them",
    "this",
    "previous",
    "same",
    "again",
    "its"
]


def is_follow_up(question):

    question = normalize(question)

    for word in FOLLOW_UP_WORDS:
        if re.search(rf"\b{word}\b", question):
            return True

    return False


# ---------------------------------------
# Local Router
# ---------------------------------------

def detect_local_intent(question):

    question = normalize(question)

    best_intent = None
    best_score = 0

    for intent, keywords in LOCAL_INTENTS.items():

        for keyword in keywords:

            if keyword in question:

                score = len(keyword)

                if score > best_score:
                    best_score = score
                    best_intent = intent

    if best_intent:
        return best_intent, 1.0

    return None, 0.0


# ---------------------------------------
# AI Router
# ---------------------------------------

def detect_ai_intent(question):

    prompt = f"""
You are an Intent Classification Engine.

Choose ONLY one function.

Functions:

{AVAILABLE_FUNCTIONS}

Return ONLY the function name.

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content.strip().split()[0]

    if answer not in AVAILABLE_FUNCTIONS:
        return "dashboard_summary"

    return answer


# ---------------------------------------
# Main Router
# ---------------------------------------

def detect_intent(question):

    if is_follow_up(question):

        last = memory.last()

        if last:

            print("🧠 Using Conversation Memory")

            return last["intent"]

    intent, confidence = detect_local_intent(question)

    if confidence >= 0.90:

        print("✅ Local Router")

        return intent

    print("🤖 AI Router")

    return detect_ai_intent(question)