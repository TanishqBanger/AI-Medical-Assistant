"""
LLM-based Agent Router.

Classifies the user's request and extracts
useful routing information.
"""

import json

from backend.ai.llm import ask_llm


# =========================================================
# ROUTER PROMPT
# =========================================================

ROUTER_SYSTEM_PROMPT = """
You are an intent classification router for CityCare Hospital.

Your job is ONLY to classify the user's request.

Choose exactly one intent:

1. hospital
   Use for:
   - Hospital FAQs
   - Hospital policies
   - Visiting hours
   - Billing
   - Insurance
   - Hospital services
   - Reception
   - General hospital information

2. medical
   Use for:
   - Symptoms
   - General medical questions
   - Health concerns
   - Medical guidance
   - Medical urgency
   - Asking what a symptom could mean

3. appointment
   Use for:
   - Finding doctors
   - Doctor availability
   - Specialists
   - Cardiologists
   - Neurologists
   - Orthopedists
   - Booking appointments
   - Scheduling appointments

DEPARTMENT MAPPING:

cardiologist → Cardiology
cardiology → Cardiology

neurologist → Neurology
neurology → Neurology

orthopedist → Orthopedics
orthopedic → Orthopedics
orthopedics → Orthopedics

If no department is mentioned or can be inferred,
set department to null.

IMPORTANT:

- Do not answer the user's question.
- Do not provide medical advice.
- Return ONLY valid JSON.
- Do not use markdown.
- Do not add explanations.

The JSON must contain exactly these fields:

{
    "intent": "hospital | medical | appointment",
    "department": "string or null"
}

Examples:

User:
"What are the hospital visiting hours?"

Output:
{"intent":"hospital","department":null}

User:
"I have a headache."

Output:
{"intent":"medical","department":null}

User:
"I want a cardiologist."

Output:
{"intent":"appointment","department":"Cardiology"}

User:
"When is the neurologist available?"

Output:
{"intent":"appointment","department":"Neurology"}

User:
"Can I book an appointment?"

Output:
{"intent":"appointment","department":null}
"""


# =========================================================
# CLASSIFY REQUEST
# =========================================================

def classify_request(message: str) -> dict:
    """
    Classify the request and extract routing information.

    Returns:

    {
        "intent": "hospital",
        "department": None
    }
    """

    messages = [
        {
            "role": "system",
            "content": ROUTER_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": message
        }
    ]

    response = ask_llm(
        messages
    )

    content = response.content.strip()

    try:

        result = json.loads(
            content
        )

        intent = result.get(
            "intent"
        )

        department = result.get(
            "department"
        )

        # Validate intent
        if intent not in {
            "hospital",
            "medical",
            "appointment"
        }:
            return {
                "intent": "hospital",
                "department": None
            }

        return {
            "intent": intent,
            "department": department
        }

    except json.JSONDecodeError:

        # Safe fallback
        return {
            "intent": "hospital",
            "department": None
        }