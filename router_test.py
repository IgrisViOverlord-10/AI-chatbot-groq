from intent_router import detect_intent

while True:
    question = input("Ask: ")

    intent = detect_intent(question)

    print("\nDetected Intent:", intent)