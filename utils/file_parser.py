limport os
import json
import zipfile
import pandas as pd
import pdfplumber
import docx

def parse_any_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    content = ""

    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    elif ext == ".pdf":
        with pdfplumber.open(file_path) as pdf:
            content = "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif ext == ".json":
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
            content = json.dumps(data, indent=2)
    elif ext == ".csv":
        df = pd.read_csv(file_path)
        content = df.to_string()
    elif ext == ".docx":
        doc = docx.Document(file_path)
        content = "\n".join(para.text for para in doc.paragraphs)
    elif ext == ".zip":
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall("extracted")
            for name in zip_ref.namelist():
                content += parse_any_file(os.path.join("extracted", name))
    return content

def extract_url_and_questions(raw_text):
    lines = raw_text.strip().split("\n")
    url = next((line for line in lines if "http" in line), None)
    questions = [line.strip() for line in lines if "?" in line]
    return url, questions
