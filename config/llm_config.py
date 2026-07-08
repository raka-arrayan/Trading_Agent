import os
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

def get_llm(role="analyst", provider="ollama"):
    """
    Returns a configured LLM based on the environment and role.
    Role determines temperature:
        - analyst / manager = 0.0 (factual, deterministik)
        - debater / researcher = 0.7 (kreatif, argumentatif)
    """
    temperature = 0.7 if role in ["debater", "researcher"] else 0.0
    
    if provider == "ollama":
        # Default local model for development/smoke test
        return ChatOllama(
            model="llama3.1:latest",
            temperature=temperature,
            base_url="http://localhost:11434"
        )
    elif provider == "gemini":
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash", # Available in free tier
            temperature=temperature
        )
    elif provider == "groq":
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=temperature
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")
