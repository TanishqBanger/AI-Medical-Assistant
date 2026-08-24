# full chat flow for the AI Medical Assistant.
import json

from backend.ai.rag import rag
from backend.ai.prompts import (
    SYSTEM_PROMPT,
    FAQ_PROMPT,
    build_prompt,
)
from backend.ai.llm import ask_llm
from backend.ai.tools import TOOLS, search_doctors


def execute_tool(tool_name, arguments):
    if tool_name == "search_doctors":
        return search_doctors(
            arguments["department"]
        )

    return {
        "success": False,
        "message": f"Unknown tool: {tool_name}"
    }


def chat(question: str) -> str:
    """
    Main chat function for the AI Medical Assistant.
    Supports RAG and tool calling.
    """

    # -------------------------
    # 1. Retrieve RAG context
    # -------------------------

    context = rag.build_context(
        query=question,
        top_k=5
    )

    # -------------------------
    # 2. Build prompt
    # -------------------------

    user_prompt = build_prompt(
        FAQ_PROMPT,
        context=context,
        question=question
    )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    # -------------------------
    # 3. First LLM call
    # -------------------------

    response = ask_llm(
        messages,
        tools=TOOLS
    )

    # -------------------------
    # 4. Check for tool call
    # -------------------------

    if response.tool_calls:

        messages.append(response)

        for tool_call in response.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            # Execute actual Python tool
            tool_result = execute_tool(
                tool_name,
                arguments
            )

            # Add tool result to conversation
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result)
                }
            )

        # -------------------------
        # 5. Ask LLM for final answer
        # -------------------------

        final_response = ask_llm(
            messages
        )

        return final_response.content

    # -------------------------
    # 6. Normal RAG answer
    # -------------------------

    return response.content