from backend.database import SessionLocal
from backend.models import ChatHistory


def save_message(
    user_message: str,
    assistant_response: str,
    patient_id: int | None = None
):
    """
    Save a conversation turn into MySQL.
    """

    db = SessionLocal()

    try:
        chat = ChatHistory(
            patient_id=patient_id,
            user_message=user_message,
            assistant_response=assistant_response
        )

        db.add(chat)
        db.commit()

    finally:
        db.close()


def get_recent_history(
    limit: int = 5,
    patient_id: int | None = None
):
    """
    Retrieve recent conversation history from MySQL.
    """

    db = SessionLocal()

    try:
        query = db.query(ChatHistory)

        if patient_id is not None:
            query = query.filter(
                ChatHistory.patient_id == patient_id
            )

        history = (
            query
            .order_by(ChatHistory.id.desc())
            .limit(limit)
            .all()
        )

        # Reverse so oldest conversation comes first
        history.reverse()

        return [
            {
                "user_message": item.user_message,
                "assistant_response": item.assistant_response
            }
            for item in history
        ]

    finally:
        db.close()