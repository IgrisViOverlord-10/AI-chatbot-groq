# intent_router.py

INTENTS = {

    "highest_selling_product": [
        "highest selling product",
        "best selling product",
        "top product",
        "most sold product",
        "most sold item",
        "top selling",
        "best seller",
        "popular product",
        "highest quantity",
        "most purchased",
        "which product sold the most",
        "top clothes"
    ],

    "highest_region_sales": [
        "highest sales region",
        "best region",
        "top region",
        "highest revenue region",
        "which region",
        "region earns most",
        "highest region",
        "best performing region"
    ],

    "men_vs_women": [
        "men vs women",
        "compare men and women",
        "gender sales",
        "male vs female",
        "which gender",
        "men sales",
        "women sales"
    ],

    "total_profit": [
        "profit",
        "total profit",
        "overall profit",
        "earnings",
        "income",
        "business profit"
    ],

    "sales_summary": [
        "summary",
        "summarize",
        "overall sales",
        "sales report",
        "dashboard summary",
        "overview"
    ]
}


# -------------------------------
# Detect Intent Function
# -------------------------------

def detect_intent(question):

    question = question.lower()

    for intent, keywords in INTENTS.items():

        for keyword in keywords:

            if keyword in question:
                return intent

    return "unknown"