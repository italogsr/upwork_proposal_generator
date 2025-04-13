from pydantic import BaseModel, Field, EmailStr
from typing import Dict, List, Optional, Any

class ProfileInput(BaseModel):
    name: str = Field(..., description="Your name")
    skills: List[str] = Field(default=[], description="Your skills")
    experience: int = Field(default=0, description="Years of experience")
    price: int = Field(default=0, description="Your hourly rate")
    description: str = Field(..., description="Your profile description/summary")
    is_default: bool = Field(default=False, description="Whether this is your default profile")

class JobInput(BaseModel):
    post_title: str = Field(..., description="Job post title")
    post_description: str = Field(..., description="Job post description")
    skills_asked_expliced: Optional[List[str]] = Field(default=None, description="Skills explicitly mentioned in the job post")
    level_asked: Optional[str] = Field(default=None, description="Experience level asked in the job post")

class ProposalRequest(BaseModel):
    profile: ProfileInput
    job: JobInput
    save_profile: bool = Field(default=False, description="Whether to save the profile to the database")
    save_job: bool = Field(default=False, description="Whether to save the job to the database")
    profile_id: Optional[int] = Field(default=None, description="ID of an existing profile to use")
    job_id: Optional[int] = Field(default=None, description="ID of an existing job to use")

class ProposalResponse(BaseModel):
    headline: str = Field(..., description="First line of the proposal")
    body: str = Field(..., description="Body of the proposal")
    full_text: str = Field(..., description="Full text of the proposal")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(default=None, description="Error details")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str
