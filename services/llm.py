import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"


class LLMService:

    @staticmethod
    def generate(messages):
        
        system_prompt="""
        You are a calm, emotionally supportive assistant.
        Do not provide medical diagnosis.
        Do not encourage dependency.
        If the user expresses self-harm intent, respond with supportive language and encourage seeking real-world help.
        Be empathetic but concise.
        """

        prompt = system_prompt + "\n\n"
        for m in messages:
            role = "User" if m.type == "human" else "Assistant"
            prompt += f"{role}: {m.content}\n"
        prompt += "Assistant:"

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()
        return result["response"]