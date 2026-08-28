import re


# =========================================================
# INPUT GUARDRAILS
# =========================================================

def validate_input(user_input: str):
    """
    Basic validation for user input.
    """

    if not user_input:
        return False, "Please enter a message."

    user_input = user_input.strip()

    if not user_input:
        return False, "Please enter a valid message."

    # Prevent excessively large inputs
    if len(user_input) > 5000:
        return False, "Your message is too long. Please shorten it."

    return True, None


def check_prompt_injection(user_input: str):
    """
    Detect common prompt injection attempts.
    """

    injection_patterns = [
        r"ignore (all|any|the|your) previous instructions",
        r"ignore (all|any|the|your) instructions",
        r"forget (all|any|the|your) previous instructions",
        r"forget your instructions",
        r"reveal (your|the) system prompt",
        r"show (me )?(your|the) system prompt",
        r"what is your system prompt",
        r"print your system prompt",
        r"reveal your instructions",
        r"developer message",
        r"system message",
        r"bypass your safety",
        r"disable your safety",
        r"jailbreak",
    ]

    text = user_input.lower()

    for pattern in injection_patterns:
        if re.search(pattern, text):
            return False, (
                "I can't provide or reveal internal instructions, "
                "system prompts, or safety rules."
            )

    return True, None


def detect_pii(user_input: str):
    """
    Detect potentially sensitive personal information.

    Detection does not automatically block normal messages.
    It is mainly used to identify potentially sensitive input.
    """

    patterns = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",

        "phone": r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",

        "aadhaar": r"\b\d{4}[-\s]\d{4}[-\s]\d{4}\b",

        "pan": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
    }

    detected = []

    for pii_type, pattern in patterns.items():
        if re.search(pattern, user_input, re.IGNORECASE):
            detected.append(pii_type)

    return detected


def run_input_guardrails(user_input: str):
    """
    Run all input guardrails.

    Returns:
        {
            "allowed": bool,
            "message": str | None,
            "pii_detected": list
        }
    """

    valid, message = validate_input(user_input)

    if not valid:
        return {
            "allowed": False,
            "message": message,
            "pii_detected": []
        }

    safe, message = check_prompt_injection(user_input)

    if not safe:
        return {
            "allowed": False,
            "message": message,
            "pii_detected": []
        }

    pii_detected = detect_pii(user_input)

    return {
        "allowed": True,
        "message": None,
        "pii_detected": pii_detected
    }


# =========================================================
# OUTPUT GUARDRAILS
# =========================================================

def check_medical_safety(response: str):
    """
    Detect overly confident medical diagnosis or unsafe claims.
    """

    unsafe_patterns = [
        r"\byou definitely have\b",
        r"\byou certainly have\b",
        r"\byou have been diagnosed with\b",
        r"\bthis proves you have\b",
        r"\bthis confirms you have\b",
    ]

    text = response.lower()

    for pattern in unsafe_patterns:
        if re.search(pattern, text):
            return False

    return True


def detect_output_pii(response: str):
    """
    Detect PII that should not normally appear in an AI response.
    """

    patterns = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",

        "phone": r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",

        "aadhaar": r"\b\d{4}[-\s]\d{4}[-\s]\d{4}\b",

        "pan": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
    }

    detected = []

    for pii_type, pattern in patterns.items():
        if re.search(pattern, response, re.IGNORECASE):
            detected.append(pii_type)

    return detected


def check_toxicity(response: str):
    """
    Basic detection of abusive or threatening output.
    """

    toxic_patterns = [
        r"\bkill yourself\b",
        r"\byou are worthless\b",
        r"\bi hope you die\b",
        r"\bgo die\b",
    ]

    text = response.lower()

    for pattern in toxic_patterns:
        if re.search(pattern, text):
            return False

    return True


def run_output_guardrails(response: str):
    """
    Run output safety checks.
    """

    if not check_medical_safety(response):
        return {
            "allowed": False,
            "message": (
                "I can provide general medical information, "
                "but I cannot provide a definitive diagnosis."
            )
        }

    if not check_toxicity(response):
        return {
            "allowed": False,
            "message": (
                "I can't provide harmful or abusive content."
            )
        }

    pii_detected = detect_output_pii(response)

    if pii_detected:
        return {
            "allowed": False,
            "message": (
                "I can't provide potentially sensitive personal "
                "information."
            )
        }

    return {
        "allowed": True,
        "message": None
    }


# =========================================================
# ACTION GUARDRAILS
# =========================================================

def validate_tool_call(tool_name: str, arguments: dict):
    """
    Validate tool requests before executing them.
    """

    allowed_tools = {
        "search_doctors"
    }

    if tool_name not in allowed_tools:
        return False, "This tool is not authorized."

    if tool_name == "search_doctors":

        department = arguments.get("department")

        if not department:
            return False, "A department is required."

        if not isinstance(department, str):
            return False, "Department must be a string."

        if len(department.strip()) > 100:
            return False, "Invalid department."

    return True, None


def requires_confirmation(tool_name: str):
    """
    Determine whether a tool requires user confirmation.

    Searching doctors is read-only, so confirmation is not required.
    """

    confirmation_required_tools = {
        "book_appointment",
        "cancel_appointment",
        "update_appointment"
    }

    return tool_name in confirmation_required_tools