from backend.ai.chat import chat


def handle_message(message: str) -> str:
    """
    Central orchestrator for the AI Medical Assistant.

    For now, every request is handled by the RAG + LLM chat service.
    Later, this function will route requests to different tools.
    """

    response = chat(message)

    return response