import google.generativeai as genai
import os

# Configure Gemini with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Use the correct model name (latest supported)
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

def answer_question(question, context):
    try:
        prompt = f"Context:\n{context}\n\nQuestion: {question}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error answering question: {e}"

