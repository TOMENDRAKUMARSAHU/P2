import google.generativeai as genai
import os
import time

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

def ask_gemini(context, question):
    prompt = f"""You are an AI assistant. Based on the following context, answer the question precisely.

Context:
{context}

Question:
{question}
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"

def is_uncertain(answer):
    uncertain_phrases = [
        "not available", "not enough context", "cannot determine", 
        "the provided text does not", "unknown", "can't tell", "not found"
    ]
    return any(p in answer.lower() for p in uncertain_phrases)

def answer_questions_with_retry(questions, file_text, scraped_text, max_retries=2):
    qa_pairs = []
    context = f"{file_text}\n\n{scraped_text}"

    for q in questions:
        retries = 0
        while retries <= max_retries:
            answer = ask_gemini(context, q)
            if not is_uncertain(answer):
                break
            retries += 1
            time.sleep(2)
        qa_pairs.append((q, answer))

    return qa_pairs
