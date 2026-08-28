"""
Medical Information Agent.

Handles:
- General symptoms
- General medical information
- Department suggestions

Does not provide definitive diagnoses.
"""

from backend.ai.rag import rag

from backend.ai.prompts import (
    SYSTEM_PROMPT,
    SYMPTOM_PROMPT,
    build_prompt,
)

from backend.ai.llm import ask_llm


def medical_agent(question: str, history=None) -> str:
    """
    Handle general medical questions.
    """

    context = rag.build_context(
        query=question,
        top_k=5
    )

    user_prompt = build_prompt(
        SYMPTOM_PROMPT,
        symptoms=question
    )

    user_prompt += f"""

Hospital Information:

{context}
"""

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # Add conversation history
    if history:

        for item in history:

            messages.append(
                {
                    "role": "user",
                    "content": item["user_message"]
                }
            )

            messages.append(
                {
                    "role": "assistant",
                    "content": item["assistant_response"]
                }
            )

    messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    response = ask_llm(
        messages
    )

    return response.content