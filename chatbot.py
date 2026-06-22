from router import detect_intent
from analysis import *
from explainer import explain
from memory import memory


# ----------------------------------------
# Map intents to analysis functions
# ----------------------------------------

INTENT_FUNCTIONS = {

    "highest_selling_product": highest_selling_product,
    "lowest_selling_product": lowest_selling_product,
    "top_products": top_products,

    "highest_region_sales": highest_region_sales,
    "region_sales": region_sales,

    "men_vs_women": men_vs_women,

    "sales_by_payment": sales_by_payment,
    "sales_by_category": sales_by_category,
    "sales_by_age_group": sales_by_age_group,

    "top_payment_method": top_payment_method,
    "top_age_group": top_age_group,
    "best_category": best_category,
    "most_profitable_product": most_profitable_product,
    "sales_growth": sales_growth,

    "total_sales": total_sales,
    "total_profit": total_profit,
    "total_orders": total_orders,

    "average_order_value": average_order_value,

    "dashboard_summary": dashboard_summary,
}


# ----------------------------------------
# Process User Question
# ----------------------------------------

def process_question(question):

    # Detect intent
    intent = detect_intent(question)

    print(f"\nDetected Intent: {intent}")

    # Run analysis
    analysis_function = INTENT_FUNCTIONS.get(intent)

    if analysis_function:
        data = analysis_function()
    else:
        intent = "dashboard_summary"
        data = dashboard_summary()

    # ----------------------------------------
    # Extract useful parameters
    # ----------------------------------------

    parameters = {}

    if isinstance(data, dict):

        if "product" in data:
            parameters["product"] = data["product"]

        if "region" in data:
            parameters["region"] = data["region"]

        if "category" in data:
            parameters["category"] = data["category"]

        if "payment_method" in data:
            parameters["payment_method"] = data["payment_method"]

        if "age_group" in data:
            parameters["age_group"] = data["age_group"]

    # Retrieve previous conversation
    history = memory.get_context()

    # Ask AI to explain
    answer = explain(
        intent=intent,
        data=data,
        history=history,
        parameters=parameters
    )

    # Save conversation
    memory.add(
        question=question,
        intent=intent,
        data=data,
        answer=answer,
        parameters=parameters
    )

    print(f"📌 Memory Size: {memory.size()} conversation(s)")

    return answer


# ----------------------------------------
# Main Program
# ----------------------------------------

def main():

    print("=" * 60)
    print("📊 AI Power BI Business Assistant")
    print("=" * 60)

    print("\nExample Questions:\n")

    examples = [
        "Which product sold the most?",
        "Show top 5 products",
        "Which product sold the least?",
        "Which region has the highest sales?",
        "Show sales by region",
        "Compare men and women sales",
        "Sales by category",
        "Sales by payment method",
        "Sales by age group",
        "Which payment method is used the most?",
        "Which age group generates the highest sales?",
        "Which product earns the highest profit?",
        "Which category performs the best?",
        "What is the sales growth?",
        "Total sales",
        "Total profit",
        "Total orders",
        "Average order value",
        "Dashboard summary",
        "exit"
    ]

    for item in examples:
        print(f"• {item}")

    print()

    while True:

        question = input("Ask: ").strip()

        if not question:
            print("⚠ Please enter a question.\n")
            continue

        if question.lower() in ["exit", "quit"]:
            print("\n👋 Goodbye!")
            break

        try:

            print("\n🔍 Detecting intent...")
            print("📈 Running analysis...")
            print("🤖 Generating explanation...")

            answer = process_question(question)

            print("\n" + "=" * 60)
            print(answer)
            print("=" * 60)

        except KeyboardInterrupt:
            print("\n\n👋 Session terminated.")
            break

        except Exception as e:
            print("\n❌ Something went wrong.")
            print(f"Details: {e}")


if __name__ == "__main__":
    main()