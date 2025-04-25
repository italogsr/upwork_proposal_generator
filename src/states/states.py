from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any

class InfoProfile(BaseModel):
    name: str = Field(..., description="Name of the profile")
    skills: List[str] = Field(..., description="Skills of the profile")
    experience: int = Field(..., description="Experience of the profile")
    price: int = Field(..., description="Price of the profile")
    description: str = Field(..., description="Description of the profile")

class Jobdescription(BaseModel):
    post_title: str = Field(..., description="Title of the job")
    post_description: str = Field(..., description="Description of the job")
    post_skills_founded: List[str] = Field(..., description="Skills found in the job description")	
    skills_asked_expliced: Optional[List[str]] = Field(..., description="Skills asked in the job description")
    level_asked: Optional[str] = Field(..., description="Level asked in the job description")

class ProposalState(BaseModel):
    full_text:str = Field(..., description="Full text of the Proposal.")
    