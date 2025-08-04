
from flask import Flask, request, render_template
from gemini_qa import extract_url_and_questions, answer_questions_with_retry
from utils.scraper import scrape_website
from utils.file_parser import parse_any_file, extract_url_and_questions
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        file = request.files["file"]
        filepath = os.path.join("uploads", file.filename)
        os.makedirs("uploads", exist_ok=True)
        file.save(filepath)

        file_text = parse_any_file(filepath)
        url, questions = extract_url_and_questions(file_text)

        scraped_text = scrape_website(url)
        qa_pairs = answer_questions_with_retry(questions, file_text, scraped_text)

        result = {"url": url, "qa": qa_pairs}
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
