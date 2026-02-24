import os
from dotenv import load_dotenv
from crewai.tools import tool
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

@tool("Read Financial Document")
def read_financial_document(file_path: str) -> str:
    """
    Tool to read and extract text from a PDF financial document at the given file path.
    Args:
        file_path (str): The exact path of the pdf file to read.
    Returns:
        str: The extracted text from the PDF document.
    """
    try:
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        full_report = ""
        for data in docs:
            content = data.page_content
            # Clean and format the financial document data
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")
            full_report += content + "\n"
            
        return full_report
    except Exception as e:
        return f"Error reading document: {str(e)}"