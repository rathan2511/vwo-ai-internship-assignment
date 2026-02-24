from crewai import Task
from agents import verifier, financial_analyst, investment_advisor, risk_assessor
from tools import read_financial_document

verification = Task(
    description=(
        "Read the file located at {file_path}. Verify if it is a valid financial document. "
        "Extract the company name, report date, and document type. Do not make up any information."
    ),
    expected_output="A brief summary confirming document validity, company name, and report type.",
    agent=verifier,
    async_execution=False
)

analyze_financial_document = Task(
    description=(
        "Using the document at {file_path}, thoroughly address the user's query: '{query}'. "
        "Extract key financial metrics, revenues, and operational highlights."
    ),
    expected_output=(
        "A detailed, professional financial analysis addressing the query using strictly "
        "the data found in the document. Include bullet points for key metrics."
    ),
    agent=financial_analyst,
    async_execution=False,
)

investment_analysis = Task(
    description=(
        "Based on the analysis of the document at {file_path}, formulate a logical "
        "investment perspective addressing the query: '{query}'. Do not recommend fake products."
    ),
    expected_output=(
        "A professional investment strategy and outlook based entirely on the "
        "provided financial metrics. Include cautious, data-backed recommendations."
    ),
    agent=investment_advisor,
    async_execution=False,
)

risk_assessment = Task(
    description=(
        "Review the document at {file_path} and identify genuine risk factors. "
        "Consider the user's query: '{query}'."
    ),
    expected_output=(
        "A structured risk assessment highlighting actual market, operational, or "
        "financial risks found in the text."
    ),
    agent=risk_assessor,
    async_execution=False,
)