
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-pro")


def answer_question(question, context):
    try:
        prompt = f"Context: {context}\n\nQuestion: {question}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error answering question: {e}"
