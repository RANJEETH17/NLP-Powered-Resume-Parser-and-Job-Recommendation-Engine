import spacy
import docx
from PyPDF2 import PdfReader

# Load the spaCy NLP model (English)
nlp = spacy.load("en_core_web_sm")

# List of sample skills to look for (can be extended)
SKILLS = ["python", "java", "machine learning", "flask", "html", "css", "mongodb", "react", "docker", "git", "sql", "tensorflow"]

def parse_resume(file):
    file_extension = file.filename.split('.')[-1].lower()
    if file_extension == 'pdf':
        return extract_text_from_pdf(file)
    elif file_extension == 'docx':
        return extract_text_from_docx(file)
    else:
        return []

def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return extract_skills(text)

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text
    return extract_skills(text)

def extract_skills(text):
    text = text.lower()
    extracted_skills = set()

    # Check for each skill if it's a substring in the text
    for skill in SKILLS:
        if skill in text:
            extracted_skills.add(skill)
    
    return list(extracted_skills)
