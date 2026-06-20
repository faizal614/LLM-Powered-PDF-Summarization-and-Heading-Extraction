import fitz  # PyMuPDF
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")


# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""

    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()

    return text


# Extract headings using regex
def extract_headings(text):
    lines = text.split('\n')

    headings = [
        line.strip()
        for line in lines
        if line.strip()
        and re.match(r'^[A-Z][A-Z\s:.-]{3,}$', line.strip())
    ]

    return headings


# Summarize text using Gemini
def summarize_text(text):
    prompt = f"""
Summarize the following PDF content clearly and concisely.

Content:
{text[:15000]}
"""

    response = model.generate_content(prompt)
    return response.text


# Main function
def main():
    pdf_path = "./Sample_pdfs/Resume.pdf"

    try:
        full_text = extract_text_from_pdf(pdf_path)

        print("\n--- MAIN HEADINGS ---")
        headings = extract_headings(full_text)

        if headings:
            for heading in headings:
                print(f"- {heading}")
        else:
            print("No headings found.")

        print("\n--- SUMMARY ---")
        summary = summarize_text(full_text)
        print(summary)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()