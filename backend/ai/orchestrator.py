"""
Multi-Agent Orchestrator.

Flow:

User
 ↓
Input Guardrails
 ↓
Memory
 ↓
LLM Router
 ↓
Specialized Agent
 ↓
Output Guardrails
 ↓
Memory
 ↓
User
"""

from backend.ai.hospital_agent import hospital_agent
from backend.ai.medical_agent import medical_agent
from backend.ai.appointment_agent import appointment_agent

from backend.ai.memory import (
    get_recent_history,
    save_message,
)

from backend.ai.guardrails import (
    run_input_guardrails,
    run_output_guardrails,
)

from backend.ai.router import classify_request


# =========================================================
# MAIN ORCHESTRATOR
# =========================================================

def handle_message(message: str) -> str:
    """
    Main entry point for the Multi-Agent system.
    """

    # =====================================================
    # 1. INPUT GUARDRAILS
    # =====================================================

    input_check = run_input_guardrails(
        message
    )

    if not input_check["allowed"]:

        return input_check["message"]

    # =====================================================
    # 2. LOAD MEMORY
    # =====================================================

    history = get_recent_history(
        limit=5
    )

    # =====================================================
    # 3. LLM ROUTER
    # =====================================================

    route = classify_request(
        message
    )

    agent = route["intent"]

    department = route["department"]

    print(
        f"[Router] Selected agent: {agent}"
    )

    print(
        f"[Router] Department: {department}"
    )

    # =====================================================
    # 4. EXECUTE SPECIALIZED AGENT
    # =====================================================

    if agent == "hospital":

        response = hospital_agent(
            message,
            history=history
        )

    elif agent == "medical":

        response = medical_agent(
            message,
            history=history
        )

    elif agent == "appointment":

        # appointment_agent uses the existing chat()
        # pipeline which already handles:
        #
        # - Memory
        # - RAG
        # - Tool Calling
        # - Guardrails
        #
        response = appointment_agent(
            message
        )

        return response

    else:

        # Safe fallback
        response = hospital_agent(
            message,
            history=history
        )

    # =====================================================
    # 5. OUTPUT GUARDRAILS
    # =====================================================

    output_check = run_output_guardrails(
        response
    )

    if not output_check["allowed"]:

        safe_response = output_check["message"]

        save_message(
            message,
            safe_response
        )

        return safe_response

    # =====================================================
    # 6. SAVE TO MEMORY
    # =====================================================

    save_message(
        message,
        response
    )

    # =====================================================
    # 7. RETURN RESPONSE
    # =====================================================

    return response