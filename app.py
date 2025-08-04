
from flask import Flask, render_template, request
from utils.file_parser import extract_url_and_questions, parse_any_file
from utils.scraper import scrape_website
from gemini_qa import answer_question
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    answer_list = []
    url = ""
    if request.method == "POST":
        file = request.files["file"]
        question_mode = request.form.get("question_mode", "auto")
        user_question = request.form.get("user_question", "").strip()

        if file:
            file_path = os.path.join("uploads", file.filename)
            os.makedirs("uploads", exist_ok=True)
            file.save(file_path)

            full_text = parse_any_file(file_path)
            url, questions = extract_url_and_questions(full_text)

            if question_mode == "manual" and user_question:
                questions = [user_question]

            if url:
                page_content = scrape_website(url)
                for q in questions:
                    ans = answer_question(q, page_content)
                    answer_list.append((q, ans))
            else:
                answer_list.append(("No URL found in the file.", ""))

    return render_template("index.html", answers=answer_list, url=url)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7860)
