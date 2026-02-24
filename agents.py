import os
from dotenv import load_dotenv
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import read_financial_document

# Load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ ERROR: GOOGLE_API_KEY not found!")
else:
    print(f"✅ API Key detected: {api_key[:5]}...{api_key[-5:]}")

# TRY 'gemini-1.5-flash'. If it still gives 404, change it to 'gemini-1.5-pro'
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    google_api_key=api_key,
    temperature=0
)

# Agents definitions stay exactly the same
verifier = Agent(
    role="Senior Financial Document Verifier",
    goal="Verify if the document is a legitimate financial report and extract core metadata.",
    verbose=True,
    memory=True,
    backstory="You are a strict financial compliance officer. Accuracy is your top priority.",
    tools=[read_financial_document],
    llm=llm,
    allow_delegation=True
)

financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Analyze financial data accurately to answer the query: {query}",
    verbose=True,
    memory=True,
    backstory="You provide clear, grounded insights based solely on the financial document.",
    tools=[read_financial_document],
    llm=llm,
    allow_delegation=False 
)

investment_advisor = Agent(
    role="Strategic Investment Advisor",
    goal="Provide grounded, realistic investment insights.",
    verbose=True,
    backstory="You provide cautious, data-backed investment strategies.",
    tools=[read_financial_document],
    llm=llm,
    allow_delegation=False
)

risk_assessor = Agent(
    role="Senior Risk Assessment Manager",
    goal="Identify real, documented risks within the financial report.",
    verbose=True,
    backstory="You are a conservative risk manager sticking strictly to the facts.",
    tools=[read_financial_document],
    llm=llm,
    allow_delegation=False
)