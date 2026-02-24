from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid

from crewai import Crew, Process
# FIXED: Imported all agents and tasks
from agents import verifier, financial_analyst, investment_advisor, risk_assessor
from task import verification, analyze_financial_document, investment_analysis, risk_assessment

app = FastAPI(title="Financial Document Analyzer")

def run_crew(query: str, file_path: str):
    """To run the whole crew"""
    financial_crew = Crew(
        # FIXED: Added all agents to the crew
        agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
        # FIXED: Added all tasks in a logical sequential order
        tasks=[verification, analyze_financial_document, investment_analysis, risk_assessment],
        process=Process.sequential,
        verbose=True
    )
    
    # FIXED: Passed both query and file_path into the inputs so the tasks can use them
    result = financial_crew.kickoff(inputs={'query': query, 'file_path': file_path})
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """Analyze financial document and provide comprehensive investment recommendations"""
    
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        os.makedirs("data", exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        if not query or query.strip() == "":
            query = "Analyze this financial document for investment insights"
            
        # FIXED: Ensure file_path is passed to run_crew
        response = run_crew(query=query.strip(), file_path=file_path)
        
        return {
            "status": "success",
            "query": query,
            # FIXED: CrewOutput needs to be converted to a string properly
            "analysis": getattr(response, 'raw', str(response)), 
            "file_processed": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")
    
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)