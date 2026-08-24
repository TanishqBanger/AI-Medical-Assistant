from backend.database import SessionLocal
import backend.crud as crud


def search_doctors(department: str):
    """
    Search doctors by department.
    This function is executed by Python when the LLM requests the tool.
    """

    db = SessionLocal()

    try:
        doctors = crud.get_doctors_by_department(
            db,
            department
        )

        if not doctors:
            return {
                "success": False,
                "message": f"No doctors found in {department}."
            }

        return {
            "success": True,
            "department": department,
            "doctors": [
                {
                    "id": doctor.id,
                    "name": doctor.doctor_name,
                    "department": doctor.department,
                    "experience": doctor.experience,
                    "available_days": doctor.available_days
                }
                for doctor in doctors
            ]
        }

    finally:
        db.close()
        
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_doctors",
            "description": "Search for doctors in a specific hospital department.",
            "parameters": {
                "type": "object",
                "properties": {
                    "department": {
                        "type": "string",
                        "description": "The medical department to search, such as Cardiology, Neurology, or Orthopedics."
                    }
                },
                "required": ["department"]
            }
        }
    }
]        