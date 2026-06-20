import fitz  # PyMuPDF
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# Extract all text from the PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Extract bold text only
def extract_bold_text(pdf_path):
    doc = fitz.open(pdf_path)
    bold_texts = []

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        font = span["font"]
                        text = span["text"].strip()
                        if "Bold" in font and text:
                            bold_texts.append(text)

    return list(set(bold_texts))  # Remove duplicates

# Summarize using Gemini
def summarize_text(text):
    prompt = (
        "Summarize the following PDF content clearly and concisely:\n\n"
        + text[:15000]
    )
    response = model.generate_content(prompt)
    return response.text

# === MAIN ===
pdf_path = "E:/intern/example.pdf"
full_text = extract_text_from_pdf(pdf_path)

# Extract bold text as headings
bold_headings = extract_bold_text(pdf_path)

print("\n--- BOLD TEXT HEADINGS ---")
for h in bold_headings:
    print(f"- {h}")

print("\n--- SUMMARY ---")
try:
    summary = summarize_text(full_text)
    print(summary)
except Exception as e:
    print(f"Error generating summary: {e}")
