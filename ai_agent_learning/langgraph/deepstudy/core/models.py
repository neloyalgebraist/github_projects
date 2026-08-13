import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_groq import ChatGroq

load_dotenv()

def get_orchestrator():
    """
    Mistral Small — Free & very good at structured planning.
    """
    return ChatMistralAI(
        model=os.getenv("ORCHESTRATOR_MODEL", "mistral-small-latest"),
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.3,
    )

def get_reader():
    """
    LLaMA 3.3 70B via Groq — Fast extraction.
    """
    return ChatGroq(
        model=os.getenv("READER_MODEL", "llama-3.3-70b-versatile"),
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.1,
    )

def get_critic():
    """
    LLaMA 3.3 70B via Groq — Strong reasoning.
    """
    return ChatGroq(
        model=os.getenv("CRITIC_MODEL", "llama-3.3-70b-versatile"),
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2,
    )

def get_synthesizer():
    """
    Mistral Small — Free & reliable for long context synthesis.
    """
    return ChatMistralAI(
        model=os.getenv("SYNTHESIZER_MODEL", "mistral-small-latest"),
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.4,
    )

def get_output_formatter():
    """
    LLaMA 3.1 8B via Groq — Fast polishing.
    """
    return ChatGroq(
        model=os.getenv("OUTPUT_MODEL", "llama-3.1-8b-instant"),
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3,
    )
