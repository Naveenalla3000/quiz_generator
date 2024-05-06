import os
import json
import traceback
import PyPDF2
from fpdf import FPDF

def read_file(file):
    
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"Error in reading pdf file: {e}")
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        raise Exception("File type not supported")
    


def get_table_data(quiz_json):
    quiz_data = []
    for key,value in quiz_json.items():
        mcq = value.get('mcq')
        options = [f'{key}: {val}' for key, val in value.get('options').items()]
        correct = value.get('correct')
        quiz_data.append({'MCQ':mcq,"options":options, "Correct Answer": correct})
    return quiz_data


class MCQPDF(FPDF):
    def __init__(self, include_answers=True):
        super().__init__()
        self.include_answers = include_answers
        self.title_added = False
        self.add_page()
        self.set_auto_page_break(auto=True, margin=30)

    def header(self):
        title = 'MCQ Assessment - Answers Included' if self.include_answers else 'MCQ Assessment - For Students'
        if not self.title_added:
            self.set_font('Arial', 'I', 16)
            self.cell(0, 10, title, 0, 1, 'C')
            self.cell(0, 10, '', 0, 1, 'C')
            self.title_added = True

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Generated by Hana-AI', 0, 0, 'L')
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

    def create_document(self,data):
        self.set_font("Arial", size=12)
        for key, value in data.items():
            self.set_font("Arial", 'B', 12)
            self.multi_cell(0, 10, f"Question {key}: {value['mcq']}")
            self.set_font("Arial", size=12)
            for opt_key, opt_value in value['options'].items():
                self.multi_cell(0, 10, f"{opt_key}: {opt_value}")
            if self.include_answers:
                self.multi_cell(0, 10, f"Correct Answer: {value['correct']}")
            self.ln(10)
