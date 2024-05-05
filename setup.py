from setuptools import find_packages, setup

setup(
    name='quizgenerator',
    version='0.0.1',
    author='Naveen alla',
    author_email='naveenalla3000@gmail.com',
    install_requires=[
        "langchain-google-genai",
        "langchain",
        "pandas",
        "python-dotenv",
        "fpdf",
        "pyPDF2",
        "solara"
    ],
    packages=find_packages(),
)