from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from starlette.responses import JSONResponse
import asyncio

from src.api.models import ProposalRequest, ProposalResponse, ErrorResponse
from src.states.states import InfoProfile, Jobdescription
from src.agent.proposal_agent import run_proposal_agent

# Load environment variables
load_dotenv()

# Get API key from environment
def get_api_key():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="API key not found. Please set the GROQ_API_KEY environment variable."
        )
    return api_key

# Create FastAPI app
app = FastAPI(
    title="Upwork Proposal Generator API",
    description="API for generating Upwork proposals based on profile and job description",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Upwork Proposal Generator API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/generate-proposal", response_model=ProposalResponse, responses={500: {"model": ErrorResponse}})
async def generate_proposal(
    request: ProposalRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(get_api_key)
):
    try:
        # Convert request models to internal states
        profile = InfoProfile(**request.profile.dict())
        job = Jobdescription(**request.job.dict())
        
        # Run the proposal agent with increased timeout
        proposal = await asyncio.wait_for(
            asyncio.to_thread(run_proposal_agent, profile, job, api_key),
            timeout=180  # 3 minutes timeout
        )
        
        # Return the proposal
        return ProposalResponse(
            headline=proposal.headline,
            body=proposal.body,
            full_text=proposal.full_text
        )
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="Request timed out. Please try again."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating proposal: {str(e)}"
        )
