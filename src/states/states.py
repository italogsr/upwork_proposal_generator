from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any

class InfoProfile(BaseModel):
    name: str
    skills: List[str] = []
    experience: int = 0
    price: int = 0
    description: str = ""

class Jobdescription(BaseModel):
    post_title: str = ""
    post_description: str = ""
    post_skills_founded: List[str] = []	
    skills_asked_expliced: Optional[List[str]] = []
    level_asked: Optional[str] = ""

class ProposalState(BaseModel):
    headline: str = Field(..., description="Fist Line of the Proposal. Shuld get the attention of the client.")
    body: str = Field(..., description="Body of the Proposal. Should contain the details of the proposal.")
    full_text:str = Field(..., description="Full text of the Proposal.")
    