from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
from langchain_google_genai import ChatGoogleGenerativeAI

def get_model() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview")