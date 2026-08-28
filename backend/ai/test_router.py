from backend.ai.router import classify_request


tests = [
    "What are the hospital visiting hours?",
    "I have a severe headache.",
    "I want a cardiologist.",
    "Can I book an appointment?",
    "Does the hospital accept insurance?",
    "I have chest pain and difficulty breathing.",
    "When is Dr. Amit Sharma available?",
    "I need a neurologist.",
    "I want to see an orthopedic doctor.",
]


print("\n")
print("=" * 60)
print("STRUCTURED LLM AGENT ROUTER TEST")
print("=" * 60)


for question in tests:

    result = classify_request(
        question
    )

    print(
        f"\nQuestion: {question}"
    )

    print(
        f"Intent: {result['intent']}"
    )

    print(
        f"Department: {result['department']}"
    )