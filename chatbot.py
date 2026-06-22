from router import detect_intent
from analysis import *
from explainer import explain
from memory import memory


# =====================================================
# Intent -> Analysis Function Mapping
# =====================================================

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


# =====================================================
# Process User Question
# =====================================================

def process_question(question):

    intent = detect_intent(question)

    print(f"\n✅ Intent Detected : {intent}")

    analysis_function = INTENT_FUNCTIONS.get(intent)

    if analysis_function:
        data = analysis_function()
    else:
        intent = "dashboard_summary"
        data = dashboard_summary()

    parameters = {}

    if isinstance(data, dict):

        for key in [
            "product",
            "region",
            "category",
            "payment_method",
            "age_group"
        ]:
            if key in data:
                parameters[key] = data[key]

    history = memory.get_context()

    answer = explain(
        intent=intent,
        data=data,
        history=history,
        parameters=parameters
    )

    memory.add(
        question=question,
        intent=intent,
        data=data,
        answer=answer,
        parameters=parameters
    )

    return answer


# =====================================================
# Welcome Screen
# =====================================================

def show_banner():

    print("=" * 65)
    print("📊 AI Power BI Business Assistant")
    print("=" * 65)

    print("\n💬 Try asking:\n")

    examples = [
        "Which product sold the most?",
        "Which region generated the highest sales?",
        "Compare sales between men and women.",
        "What is the total profit?",
        "Give me a dashboard summary."
    ]

    for example in examples:
        print(f"  • {example}")

    print("\n(Type 'exit' to quit)\n")


# =====================================================
# Main
# =====================================================

def main():

    show_banner()

    while True:

        question = input("📝 Ask: ").strip()

        if not question:
            print("⚠️ Please enter a question.\n")
            continue

        if question.lower() in ["exit", "quit"]:
            print("\n👋 Thank you for using AI Power BI Assistant.")
            break

        try:

            print("\n🔍 Understanding your question...")
            print("📈 Running business analysis...")
            print("🤖 Generating AI response...\n")

            answer = process_question(question)

            print("=" * 65)
            print(answer)
            print("=" * 65)

        except KeyboardInterrupt:
            print("\n\n👋 Session terminated.")
            break

        except Exception as e:
            print("\n❌ Unexpected Error")
            print(e)


if __name__ == "__main__":
    main()