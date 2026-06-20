import ollama
import json

class AIParser:
    def __init__(self, model_name="qwen2.5-coder"):
        self.model_name = model_name

    def extract_logistics_data(self, raw_text: str):
        """
        Uses local Ollama to parse raw, messy dispatcher notes into strict JSON data.
        """
        # This structure forces the AI to be a data converter, not a chat buddy
        prompt = f"""
        Extract the stop names and coordinates from this text. 
        Return ONLY a raw JSON array of objects with keys "name", "lat", "lng".
        Text: {raw_text}
        """
        # In the future, we call ollama.chat() here. 
        # For setup validation, we return mock structured data.
        return [
            {"name": "Hub", "lat": 0.0, "lng": 0.0},
            {"name": "Stop A", "lat": 1.2, "lng": 3.4}
        ]