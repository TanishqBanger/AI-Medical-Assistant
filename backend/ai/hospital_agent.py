"""
Hospital Information Agent.

Handles:
- Hospital FAQs
- Hospital policies
- Visiting hours
- Hospital services
- Billing
- General hospital information
"""

from backend.ai.rag import rag

from backend.ai.prompts import (
    SYSTEM_PROMPT,
    FAQ_PROMPT,
    build_prompt,
)

from backend.ai.llm import ask_llm


def hospital_agent(question: str, history=None) -> str:
    """
    Answer hospital-related questions using RAG.
    """

    context = rag.build_context(
        query=question,
        top_k=5
    )

    user_prompt = build_prompt(
        FAQ_PROMPT,
        context=context,
        question=question
    )

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