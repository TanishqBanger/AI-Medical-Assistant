# Full chat flow for the AI Medical Assistant.

import json

from backend.ai.rag import rag

from backend.ai.prompts import (
    SYSTEM_PROMPT,
    FAQ_PROMPT,
    build_prompt,
)

from backend.ai.llm import ask_llm

from backend.ai.tools import (
    TOOLS,
    search_doctors,
)

from backend.ai.memory import (
    get_recent_history,
    save_message,
)

from backend.ai.guardrails import (
    run_input_guardrails,
    run_output_guardrails,
    validate_tool_call,
)


# =========================================================
# TOOL EXECUTION
# =========================================================

def execute_tool(tool_name, arguments):
    """
    Execute an authorized tool.
    """

    if tool_name == "search_doctors":
        return search_doctors(
            arguments["department"]
        )

    return {
        "success": False,
        "message": f"Unknown tool: {tool_name}"
    }


# =========================================================
# MAIN CHAT FUNCTION
# =========================================================

def chat(question: str) -> str:
    """
    Main chat function for the AI Medical Assistant.

    Flow:

    Input Guardrails
        ↓
    Memory
        ↓
    RAG
        ↓
    LLM + Tool Calling
        ↓
    Action Guardrails
        ↓
    Tool Execution
        ↓
    Final LLM Response
        ↓
    Output Guardrails
        ↓
    Memory
        ↓
    Final Answer
    """

    # =====================================================
    # 1. INPUT GUARDRAILS
    # =====================================================

    input_check = run_input_guardrails(question)

    if not input_check["allowed"]:
        return input_check["message"]

    # =====================================================
    # 2. RETRIEVE RAG CONTEXT
    # =====================================================

    context = rag.build_context(
        query=question,
        top_k=5
    )

    # =====================================================
    # 3. BUILD PROMPT
    # =====================================================

    user_prompt = build_prompt(
        FAQ_PROMPT,
        context=context,
        question=question
    )

    # =====================================================
    # 4. LOAD CONVERSATION MEMORY
    # =====================================================

    history = get_recent_history(
        limit=5
    )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

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

    # =====================================================
    # 5. FIRST LLM CALL
    # =====================================================

    response = ask_llm(
        messages,
        tools=TOOLS
    )

    # =====================================================
    # 6. TOOL CALLING
    # =====================================================

    if response.tool_calls:

        messages.append(response)

        for tool_call in response.tool_calls:

            tool_name = tool_call.function.name

            try:
                arguments = json.loads(
                    tool_call.function.arguments
                )
            except json.JSONDecodeError:

                tool_result = {
                    "success": False,
                    "message": "Invalid tool arguments."
                }

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result)
                    }
                )

                continue

            # =================================================
            # ACTION GUARDRAIL
            # =================================================

            tool_check = validate_tool_call(
                tool_name,
                arguments
            )

            if not tool_check[0]:

                tool_result = {
                    "success": False,
                    "message": tool_check[1]
                }

            else:

                # =============================================
                # EXECUTE AUTHORIZED TOOL
                # =============================================

                tool_result = execute_tool(
                    tool_name,
                    arguments
                )

            # =================================================
            # SEND TOOL RESULT BACK TO LLM
            # =================================================

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result)
                }
            )

        # =====================================================
        # 7. FINAL LLM CALL
        # =====================================================

        final_response = ask_llm(
            messages
        )

        answer = final_response.content

    else:

        # =====================================================
        # 7. NORMAL RAG ANSWER
        # =====================================================

        answer = response.content

    # =========================================================
    # 8. OUTPUT GUARDRAILS
    # =========================================================

    output_check = run_output_guardrails(
        answer
    )

    if not output_check["allowed"]:

        safe_response = output_check["message"]

        save_message(
            question,
            safe_response
        )

        return safe_response

    # =========================================================
    # 9. SAVE APPROVED RESPONSE TO MEMORY
    # =========================================================

    save_message(
        question,
        answer
    )

    # =========================================================
    # 10. RETURN FINAL RESPONSE
    # =========================================================

    return answer