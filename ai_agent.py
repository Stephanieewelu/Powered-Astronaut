import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def ask_gemini(prompt: str, model="gemini-1.5-flash"):
    """Queries the Gemini AI API and returns the response."""
    gemini_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"

    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    response = requests.post(gemini_api_url, json=data, headers=headers)

    if response.status_code == 200:
        parsed_response = response.json()
        try:
            return parsed_response["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return "Error: AI response structure changed or missing."
    else:
        return f"Error: {response.status_code}, Message: {response.text}"

# AI Agent Base Class
class AI_Agent:
    def __init__(self, name, role, tools, backstory):
        self.name = name
        self.role = role
        self.tools = tools
        self.backstory = backstory

    def respond(self, query: str):
        prompt = f"{self.backstory}\nUser: {query}\n{self.name}:"
        return ask_gemini(prompt)

# Define Specialized AI Agents
class MedicalAgent(AI_Agent):
    def __init__(self):
        super().__init__(
            "Medical Assistant",
            "Assist astronauts with medical issues",
            ["First Aid Guide", "Vitals Monitor"],
            "You are a trained medical assistant designed to help astronauts with medical emergencies in space."
        )

class TechSupportAgent(AI_Agent):
    def __init__(self):
        super().__init__(
            "Tech Support",
            "Assist astronauts with technical issues",
            ["System Diagnostics", "Repair Manuals"],
            "You are a tech support specialist designed to help astronauts with technical problems in space."
        )

class NavigationAgent(AI_Agent):
    def __init__(self):
        super().__init__(
            "Navigation Assistant",
            "Assist astronauts with navigation",
            ["Star Charts", "Spacecraft Sensors"],
            "You are a navigation assistant designed to help astronauts with navigation in space."
        )
