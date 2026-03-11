import os
import sys

# load dotenv to simulate app.py
from dotenv import load_dotenv
load_dotenv(os.path.join("backend", ".env"))

from backend.services.ai_service import AIService

try:
    print("Testing extraction...")
    result = AIService.extract_tasks_from_notes("Meeting notes\n- Do the laundry\n- Take out trash")
    print("RESULT:", result)
except Exception as e:
    print("RAISED EXCEPTION:", type(e), str(e))
