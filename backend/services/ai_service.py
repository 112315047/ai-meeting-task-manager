import os
import json
import logging
from datetime import datetime, timezone, timedelta
import re

try:
    from groq import Groq
except ImportError:
    # Fallback if pip is broken and groq package cannot be installed:
    # Use the existing openai package configured for Groq's compatible API
    from openai import OpenAI
    class Groq(OpenAI):
        def __init__(self, api_key=None, **kwargs):
            kwargs.setdefault("base_url", "https://api.groq.com/openai/v1")
            super().__init__(api_key=api_key, **kwargs)

logger = logging.getLogger(__name__)

# Fallback to a dummy key so the app will start if the key is missing; 
# API calls will fail gracefully but hit the internal local fallback logic.
api_key = os.getenv("GROQ_API_KEY", "dummy_key_for_fallback")
client = Groq(api_key=api_key)

def get_ist_date():
    # IST is UTC + 5:30
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    return ist_now.strftime("%Y-%m-%d")

def parse_time_from_text(text: str):
    lower_line = text.lower()
    if re.search(r'\b(now)\b', lower_line):
        ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
        return ist_now.strftime("%H:%M")
    elif re.search(r'\b(sleep)\b', lower_line):
        return "22:00"
    elif re.search(r'\b(early)\b', lower_line):
        return "06:00"
    elif re.search(r'\b(late|lately)\b', lower_line):
        return "10:00"
    elif re.search(r'\b(morning)\b', lower_line):
        return "09:00"
    elif re.search(r'\b(afternoon)\b', lower_line):
        return "14:00"
    elif re.search(r'\b(evening|early evening)\b', lower_line):
        return "16:00"
    elif re.search(r'\b(night)\b', lower_line):
        return "21:00"
    elif match := re.search(r'\b(\d{1,2})\s*(am|pm)\b', lower_line):
        hour = int(match.group(1))
        ampm = match.group(2)
        if ampm == 'pm' and hour < 12:
            hour += 12
        elif ampm == 'am' and hour == 12:
            hour = 0
        return f"{hour:02d}:00"
    return None

class AIService:
    @staticmethod
    def extract_tasks_from_notes(notes: str):
        try:
            current_date = get_ist_date()
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": f"""Extract tasks from meeting notes. Return JSON array with title, description, assignee, due_date, scheduled_time.
Detect simple time expressions and map them to scheduled_time in HH:MM format (24-hour).
Detect date expressions (today, tomorrow, next week, specific days) and map them to due_date in YYYY-MM-DD format. Assume the current date is {current_date}.
Mapping rules for time:
morning -> 09:00
afternoon -> 14:00
evening -> 19:00
night -> 21:00
etc.
If no time is detected, set scheduled_time to null.
If no date is detected, set due_date to {current_date}."""
                    },
                    {
                        "role": "user",
                        "content": notes
                    }
                ]
            )
            content = response.choices[0].message.content
            
            # Parse the response text safely
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
                
            parsed = json.loads(content)
            
            # Handle if the LLM returned {"tasks": [...]} or just [...]
            if isinstance(parsed, dict) and "tasks" in parsed:
                return parsed["tasks"]
            elif isinstance(parsed, list):
                return parsed
            else:
                raise ValueError("Parsed JSON is not a valid list of tasks.")
                
        except Exception as e:
            logger.error(f"AI extraction failed, using fallback: {e}")
            
            # Replace common conjunctions with newlines to split single-line inputs into multiple tasks
            # Now also splitting on " i want to " and " i need to " so "I need to bath I want to prepare an excel sheet" splits correctly.
            text = re.sub(r'(?i)\b(also|and|then)\b', '\n', notes)
            # Add newlines before "i want to" or "i need to" if they aren't at the start of a string
            text = re.sub(r'(?i)(?<=\s)(i\s+(want|need)\s+to)\b', r'\n\1', text)
            
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            
            current_date = get_ist_date()
            tasks = []
            for line in lines:
                time_val = parse_time_from_text(line)

                tasks.append({
                    "title": line,
                    "description": f"Extracted from notes",
                    "assignee": "Unassigned",
                    "due_date": current_date,
                    "scheduled_time": time_val
                })
            return tasks
