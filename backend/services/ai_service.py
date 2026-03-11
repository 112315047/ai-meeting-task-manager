import os
import json
import logging

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

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class AIService:
    @staticmethod
    def extract_tasks_from_notes(notes: str):
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": "Extract tasks from meeting notes. Return JSON array with title, description, assignee, due_date."
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
            
            # Fallback extraction if Groq fails
            lines = [line.strip() for line in notes.split("\n") if line.strip()]
            
            tasks = []
            for line in lines:
                tasks.append({
                    "title": line,
                    "description": f"Extracted from notes: {line}",
                    "assignee": "Unassigned",
                    "due_date": None
                })
            return tasks
