from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
import os
from dotenv import load_dotenv
from starlette.responses import JSONResponse
import asyncio
from typing import List
from sqlalchemy.orm import Session
from datetime import timedelta

from src.api.models import ProposalRequest, ProposalResponse, ErrorResponse
from src.states.states import InfoProfile, Jobdescription
from src.agent.proposal_agent import run_proposal_agent
from src.db import crud, models, schemas
from src.db.database import get_db, engine
from src.api.auth import (
    create_access_token,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# Create tables
models.Base.metadata.create_all(bind=engine)

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

# Authentication endpoints
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# Profile endpoints
@app.get("/profiles/", response_model=List[schemas.ProfileResponse])
async def read_profiles(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    profiles = crud.get_profiles_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return profiles

@app.get("/profiles/default", response_model=schemas.ProfileResponse)
async def read_default_profile(
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    profile = crud.get_default_profile(db, user_id=current_user.id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Default profile not found")
    return profile

@app.post("/profiles/", response_model=schemas.ProfileResponse)
async def create_profile(
    profile: schemas.ProfileCreate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return crud.create_profile(db=db, profile=profile, user_id=current_user.id)

@app.put("/profiles/{profile_id}", response_model=schemas.ProfileResponse)
async def update_profile(
    profile_id: int,
    profile: schemas.ProfileUpdate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    updated_profile = crud.update_profile(db=db, profile_id=profile_id, profile=profile, user_id=current_user.id)
    if updated_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return updated_profile

@app.delete("/profiles/{profile_id}")
async def delete_profile(
    profile_id: int,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    success = crud.delete_profile(db=db, profile_id=profile_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"detail": "Profile deleted successfully"}

# Job description endpoints
@app.get("/jobs/", response_model=List[schemas.JobDescriptionResponse])
async def read_job_descriptions(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    jobs = crud.get_job_descriptions_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return jobs

@app.post("/jobs/", response_model=schemas.JobDescriptionResponse)
async def create_job_description(
    job: schemas.JobDescriptionCreate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return crud.create_job_description(db=db, job=job, user_id=current_user.id)

@app.put("/jobs/{job_id}", response_model=schemas.JobDescriptionResponse)
async def update_job_description(
    job_id: int,
    job: schemas.JobDescriptionUpdate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    updated_job = crud.update_job_description(db=db, job_id=job_id, job=job, user_id=current_user.id)
    if updated_job is None:
        raise HTTPException(status_code=404, detail="Job description not found")
    return updated_job

@app.delete("/jobs/{job_id}")
async def delete_job_description(
    job_id: int,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    success = crud.delete_job_description(db=db, job_id=job_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Job description not found")
    return {"detail": "Job description deleted successfully"}

# Proposal endpoints
@app.get("/proposals/", response_model=List[schemas.ProposalResponse])
async def read_proposals(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    proposals = crud.get_proposals_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return proposals

@app.post("/generate-proposal", response_model=ProposalResponse, responses={500: {"model": ErrorResponse}})
async def generate_proposal(
    request: ProposalRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(get_api_key),
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
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

        # Save profile if requested
        profile_id = None
        if request.save_profile:
            db_profile = crud.create_profile(
                db=db,
                profile=schemas.ProfileCreate(
                    name=request.profile.name,
                    skills=request.profile.skills,
                    experience=request.profile.experience,
                    price=request.profile.price,
                    description=request.profile.description,
                    is_default=request.profile.is_default if hasattr(request.profile, "is_default") else False
                ),
                user_id=current_user.id
            )
            profile_id = db_profile.id
        else:
            # Use existing profile if provided
            profile_id = request.profile_id if hasattr(request, "profile_id") else None

            # If no profile_id provided, try to use default profile
            if not profile_id:
                default_profile = crud.get_default_profile(db, user_id=current_user.id)
                if default_profile:
                    profile_id = default_profile.id

        # Save job description if requested
        job_id = None
        if request.save_job:
            db_job = crud.create_job_description(
                db=db,
                job=schemas.JobDescriptionCreate(
                    post_title=request.job.post_title,
                    post_description=request.job.post_description,
                    skills_asked_expliced=request.job.skills_asked_expliced,
                    level_asked=request.job.level_asked
                ),
                user_id=current_user.id
            )
            job_id = db_job.id
        else:
            # Use existing job if provided
            job_id = request.job_id if hasattr(request, "job_id") else None

        # Save proposal if both profile and job are saved
        if profile_id and job_id:
            crud.create_proposal(
                db=db,
                proposal=schemas.ProposalCreate(
                    profile_id=profile_id,
                    job_description_id=job_id,
                    headline=proposal.headline,
                    body=proposal.body,
                    full_text=proposal.full_text
                )
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

@app.delete("/proposals/{proposal_id}")
async def delete_proposal(
    proposal_id: int,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    success = crud.delete_proposal(db=db, proposal_id=proposal_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return {"detail": "Proposal deleted successfully"}
