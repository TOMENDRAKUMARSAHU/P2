import google.generativeai as genai
import os

# Configure Gemini with API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Use lighter + faster model to avoid quota issues
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def answer_question(question, context):
    try:
        prompt = f"Context:\n{context}\n\nQuestion: {question}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error answering question: {e}"
