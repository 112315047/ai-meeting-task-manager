import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class AIService:
    @staticmethod
    def extract_tasks_from_notes(notes: str) -> List[Dict]:
        """
        Simulates extracting actionable tasks from unstructured meeting notes using an AI model.
        Returns a list of dictionaries representing tasks.
        """
        logger.info(f"Extracting tasks from notes: {notes[:50]}...")
        
        # In a real scenario, we would call an LLM API here (e.g., OpenAI, Anthropic)
        # For now, we stub it out with a basic mock based on keyword detection 
        # just for demonstration purposes.
        
        tasks_found = []
        
        # Simple dynamic mockup: split notes by newline/bullet and generate tasks
        lines = [line.strip("-* ") for line in notes.split('\n') if line.strip()]
        
        for index, line in enumerate(lines):
            # Very basic extraction logic to prove it works dynamically based on user input
            title = line[:50] if len(line) > 50 else line
            
            # Basic assignment logic mockup
            assignee = "Backend Team" if "backend" in line.lower() else ("Frontend Team" if "frontend" in line.lower() else "Unassigned")
            
            tasks_found.append({
                "title": title.strip(),
                "description": f"Extracted from notes: {line}",
                "assignee": assignee
            })
            
        return tasks_found
