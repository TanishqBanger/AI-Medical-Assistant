#  OpenAI + hospital config
import os
from datetime import time
from dotenv import load_dotenv


load_dotenv()


# Hospital configuration
HOSPITAL_OPEN_TIME = time(9, 0)      # 09:00 AM
HOSPITAL_CLOSE_TIME = time(17, 0)    # 05:00 PM


# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")