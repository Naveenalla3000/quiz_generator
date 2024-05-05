import os
import sys
import json
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
import pandas as pd
from fpdf import FPDF
from source.quizgenerator.utils import MCQPDF
from source.quizgenerator.utils import get_table_data

load_dotenv()

KEY = os.getenv("GOOGLE_API_KEY")

llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=KEY,temperature=.7)

TEMPLATE_1='''
   TEXT: {text}
You are an expert in creating multiple choice questions. Given the above text, it is your job to create a quiz of {number} questions for {subject} students in a {tone} tone. Ensure the questions are unique and relevant to the text.
Use the format provided below as a guide to construct your quiz, making sure to include {number} MCQs:

{response_json}

'''

quiz_generation_prompt = PromptTemplate(
    input_variables=["text","number","subject","tone","response_json"],
    template=TEMPLATE_1
)

quiz_chain = LLMChain(
    llm=llm,
    prompt = quiz_generation_prompt,
    output_key = "quiz",
    # verbose=True
)

TEMPLATE_2 = '''
    You are expert in english gramer and writer. Give a muitiple choice for students in subject {subject}. \
    You need to evaluate the complexity of question and give a complete ananylsis of quiz. Only use at max 50 words for each.\
    Quiz_MCQs:
    {quiz}

    check from expert English writer of the above quiz:
'''

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject","quiz"],
    template=TEMPLATE_2
)

review_chain = LLMChain(
    llm=llm,
    prompt = quiz_evaluation_prompt,
    output_key = "review",
    # verbose=True
)

def generate_response(text,number,subject,tone,response_json):
    print("Text: ",text)
    print("Number: ",number)
    print("Subject: ",subject)
    print("Tone: ",tone)
    print("Response JSON: ",response_json)
    response = generate_evalution_chain.__call__({
        "text":text,
        "number":number,
        "subject":subject,
        "tone":tone,
        "response_json":response_json
    })
    
    quiz = response.get('quiz')
    quiz_json = json.loads(quiz)
    quiz_data = get_table_data(quiz_json)

    data = quiz_json
    pwd = os.getcwd()
    pdfs = pwd + '/media/pdfs/'
    pdf_with_answers = MCQPDF(include_answers=True)
    pdf_with_answers.set_author("Hana-AI")
    pdf_with_answers.create_document(data)
    pdf_with_answers.output(os.path.join(pdfs,'MCQs_With_With_Answers_HanaAi.pdf'))    


    pdf_without_answers = MCQPDF(include_answers=False)
    pdf_without_answers.set_author("Hana-AI")
    pdf_without_answers.create_document(data)
    pdf_without_answers.output(os.path.join(pdfs,'MCQs_By_HanaAi.pdf'))

    
    return quiz_data


generate_evalution_chain = SequentialChain(
    chains=[quiz_chain,review_chain],
    input_variables=["text","number","subject","tone","response_json"],
    output_variables=["quiz","review"],
    # verbose=True
)