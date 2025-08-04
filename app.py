from flask import Flask, request, render_template
from gemini_qa import answer_questions_with_retry
from utils.scraper import scrape_website
from utils.file_parser import (
    parse_any_file,
    extract_url_and_questions,
    convert_s3_to_https,
    try_fetch_parquet_from_url
)
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

        # Step 1: Extract file content, URL, and questions
        file_text = parse_any_file(filepath)
        url, questions = extract_url_and_questions(file_text)
        readable_url = convert_s3_to_https(url)

        # Step 2: Try fetching content (either .parquet or normal scrape)
        if readable_url.endswith(".parquet"):
            scraped_text = try_fetch_parquet_from_url(readable_url)
        else:
            scraped_text = scrape_website(readable_url)

        # Step 3: Ask Gemini with full context
        qa_pairs = answer_questions_with_retry(questions, file_text, scraped_text)

        # Step 4: Show results
        result = {"url": readable_url, "qa": qa_pairs}

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
