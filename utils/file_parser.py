import os
import zipfile
import json
import pandas as pd
import pdfplumber
import docx
import re

def extract_text_from_pdf(filepath):
    text = ""
    with fitz.open(filepath) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(filepath):
    doc = docx.Document(filepath)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return json.dumps(data, indent=2)
        except json.JSONDecodeError:
            return f.read()

def extract_text_from_csv(filepath):
    df = pd.read_csv(filepath)
    return df.to_string(index=False)

def extract_text_from_parquet(filepath):
    df = pd.read_parquet(filepath)
    return df.to_string(index=False)

def extract_text_from_txt(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def extract_text_from_zip(filepath):
    temp_dir = "temp_extracted"
    extracted_text = ""
    with zipfile.ZipFile(filepath, "r") as zip_ref:
        zip_ref.extractall(temp_dir)
        for root, _, files in os.walk(temp_dir):
            for file in files:
                full_path = os.path.join(root, file)
                extracted_text += parse_any_file(full_path) + "\n"
    return extracted_text

def parse_any_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
    with pdfplumber.open(file_path) as pdf:
        content = "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif ext == ".docx":
        return extract_text_from_docx(filepath)
    elif ext == ".json":
        return extract_text_from_json(filepath)
    elif ext == ".csv":
        return extract_text_from_csv(filepath)
    elif ext == ".parquet":
        return extract_text_from_parquet(filepath)
    elif ext == ".zip":
        return extract_text_from_zip(filepath)
    elif ext == ".txt":
        return extract_text_from_txt(filepath)
    else:
        return "Unsupported file format."

def extract_url_and_questions(text):
    url_pattern = r"(https?://\S+|s3://\S+)"
    question_pattern = r"(?:Q[:：]?\s*)([\s\S]*?)\n(?:A[:：]|$)"

    url_match = re.search(url_pattern, text)
    url = url_match.group(0).strip() if url_match else ""

    questions = [q.strip() for q in re.findall(question_pattern, text)]
    return url, questions

def convert_s3_to_https(s3_url):
    if not s3_url.startswith("s3://"):
        return s3_url
    parts = s3_url.replace("s3://", "").split("/", 1)
    bucket = parts[0]
    path = parts[1] if len(parts) > 1 else ""
    return f"https://{bucket}.s3.amazonaws.com/{path}"

def try_fetch_parquet_from_url(url):
    try:
        df = pd.read_parquet(url, engine="pyarrow")
        return df.to_string(index=False)
    except Exception as e:
        return f"Could not fetch remote parquet file: {e}"
