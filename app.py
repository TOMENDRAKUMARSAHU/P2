from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from gemini_qa import answer_questions_with_retry
from utils.scraper import scrape_website
from utils.file_parser import (
    parse_any_file,
    extract_url_and_questions,
    try_fetch_parquet_from_url
)
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        if "file" not in request.files:
            return render_template("index.html", result={"error": "No file part in request."})

        file = request.files["file"]
        if file.filename == "":
            return render_template("index.html", result={"error": "No file selected."})

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Extract file content and questions
        file_text = parse_any_file(filepath)
        url, questions = extract_url_and_questions(file_text)

        # Scrape or download data from URL
        if url and url.endswith(".parquet"):
            scraped_text = try_fetch_parquet_from_url(url)
        elif url:
            scraped_text = scrape_website(url)
        else:
            scraped_text = ""

        try:
            qa_pairs = answer_questions_with_retry(questions, file_text, scraped_text)
        except Exception as e:
            qa_pairs = [("Error", f"Failed to answer questions: {str(e)}")]

        result = {"url": url, "qa": qa_pairs}

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
