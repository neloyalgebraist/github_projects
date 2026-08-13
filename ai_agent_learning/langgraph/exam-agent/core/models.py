import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def get_model(model_name: str = "llama-3.3-70b-versatile", temperature: float = 0.1):
    """
    Returns a Groq model instance.
    70B is excellent for extraction and reasoning.
    """

    return ChatGroq(
        model=model_name,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=temperature,
    )
