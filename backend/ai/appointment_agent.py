"""
Appointment / Doctor Agent.

Handles:
- Finding doctors
- Doctor availability
- Doctor-related questions
- Appointment-related requests
"""

from backend.ai.chat import chat


def appointment_agent(question: str) -> str:
    """
    Handle doctor and appointment-related requests.

    Uses the existing tool-calling pipeline.
    """

    return chat(question)