from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Any
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Profile schemas
class ProfileBase(BaseModel):
    name: str
    skills: List[str] = []
    experience: int = 0
    price: int = 0
    description: str

class ProfileCreate(ProfileBase):
    is_default: bool = False

class ProfileUpdate(ProfileBase):
    name: Optional[str] = None
    skills: Optional[List[str]] = None
    experience: Optional[int] = None
    price: Optional[int] = None
    description: Optional[str] = None
    is_default: Optional[bool] = None

class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    is_default: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Job description schemas
class JobDescriptionBase(BaseModel):
    post_title: str
    post_description: str
    skills_asked_expliced: Optional[List[str]] = None
    level_asked: Optional[str] = None

class JobDescriptionCreate(JobDescriptionBase):
    pass

class JobDescriptionUpdate(JobDescriptionBase):
    post_title: Optional[str] = None
    post_description: Optional[str] = None
    skills_asked_expliced: Optional[List[str]] = None
    level_asked: Optional[str] = None

class JobDescriptionResponse(JobDescriptionBase):
    id: int
    user_id: int
    post_skills_founded: List[str] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Proposal schemas
class ProposalBase(BaseModel):
    headline: str
    body: str
    full_text: str

class ProposalCreate(ProposalBase):
    profile_id: int
    job_description_id: int

class ProposalResponse(ProposalBase):
    id: int
    profile_id: int
    job_description_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
