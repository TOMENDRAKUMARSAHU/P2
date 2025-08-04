
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
flash = genai.GenerativeModel("models/gemini-1.5-flash-latest")
pro = genai.GenerativeModel("models/gemini-1.5-pro-latest")

def extract_url_and_questions(text):
    import re
    url_match = re.search(r'https?://\S+', text)
    url = url_match.group(0) if url_match else ""
    question_lines = [line.strip() for line in text.splitlines() if line.strip().startswith("Q:")]
    questions = [line.split(":", 1)[1].strip() for line in question_lines]
    return url, questions

def answer_question(model, question, context):
    prompt = f"""
You are a helpful assistant. Use only the provided context.

Context:
{context}

Question: {question}

If you don't have enough information, respond with "Not enough information in context."
"""
    try:
        res = model.generate_content(prompt)
        return res.text.strip()
    except Exception as e:
        return f"Error: {e}"

def answer_questions_with_retry(questions, file_context, scraped_context):
    results = []
    full_context = file_context + "\n" + scraped_context
    for q in questions:
        print(f"🔍 Q: {q}")
        ans = answer_question(flash, q, full_context)
        if "not enough" in ans.lower() or "i don't know" in ans.lower() or len(ans) < 5:
            print("↪️ Flash unsure, retrying with Pro...")
            ans = answer_question(pro, q, full_context)
        results.append((q, ans))
    return results
