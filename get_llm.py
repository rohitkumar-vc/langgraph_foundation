from langchain_google_genai import ChatGoogleGenerativeAI

def get_model():
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", vertexai=True)