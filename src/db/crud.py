from sqlalchemy.orm import Session
from sqlalchemy import desc
from . import models, schemas
from passlib.context import CryptContext
from typing import List, Optional

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Profile operations
def get_profile(db: Session, profile_id: int):
    return db.query(models.Profile).filter(models.Profile.id == profile_id).first()

def get_profiles_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Profile).filter(models.Profile.user_id == user_id).offset(skip).limit(limit).all()

def get_default_profile(db: Session, user_id: int):
    return db.query(models.Profile).filter(models.Profile.user_id == user_id, models.Profile.is_default == True).first()

def create_profile(db: Session, profile: schemas.ProfileCreate, user_id: int):
    # If this is the first profile or marked as default, ensure it's the only default
    if profile.is_default:
        # Reset any existing default profiles
        db.query(models.Profile).filter(
            models.Profile.user_id == user_id, 
            models.Profile.is_default == True
        ).update({"is_default": False})
    
    # If no profiles exist yet, make this one default regardless
    profile_count = db.query(models.Profile).filter(models.Profile.user_id == user_id).count()
    if profile_count == 0:
        profile.is_default = True
    
    db_profile = models.Profile(
        user_id=user_id,
        name=profile.name,
        skills=profile.skills,
        experience=profile.experience,
        price=profile.price,
        description=profile.description,
        is_default=profile.is_default
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def update_profile(db: Session, profile_id: int, profile: schemas.ProfileUpdate, user_id: int):
    db_profile = db.query(models.Profile).filter(
        models.Profile.id == profile_id, 
        models.Profile.user_id == user_id
    ).first()
    
    if not db_profile:
        return None
    
    # Update profile fields if provided
    update_data = profile.dict(exclude_unset=True)
    
    # Handle default profile logic
    if "is_default" in update_data and update_data["is_default"]:
        # Reset any existing default profiles
        db.query(models.Profile).filter(
            models.Profile.user_id == user_id, 
            models.Profile.is_default == True
        ).update({"is_default": False})
    
    for key, value in update_data.items():
        setattr(db_profile, key, value)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile

def delete_profile(db: Session, profile_id: int, user_id: int):
    db_profile = db.query(models.Profile).filter(
        models.Profile.id == profile_id, 
        models.Profile.user_id == user_id
    ).first()
    
    if not db_profile:
        return False
    
    # Check if this is the default profile
    was_default = db_profile.is_default
    
    db.delete(db_profile)
    db.commit()
    
    # If we deleted the default profile, set a new one if any exist
    if was_default:
        new_default = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
        if new_default:
            new_default.is_default = True
            db.commit()
    
    return True

# Job description operations
def get_job_description(db: Session, job_id: int):
    return db.query(models.JobDescription).filter(models.JobDescription.id == job_id).first()

def get_job_descriptions_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.JobDescription).filter(
        models.JobDescription.user_id == user_id
    ).order_by(desc(models.JobDescription.created_at)).offset(skip).limit(limit).all()

def create_job_description(db: Session, job: schemas.JobDescriptionCreate, user_id: int):
    db_job = models.JobDescription(
        user_id=user_id,
        post_title=job.post_title,
        post_description=job.post_description,
        post_skills_founded=[],
        skills_asked_expliced=job.skills_asked_expliced or [],
        level_asked=job.level_asked
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def update_job_description(db: Session, job_id: int, job: schemas.JobDescriptionUpdate, user_id: int):
    db_job = db.query(models.JobDescription).filter(
        models.JobDescription.id == job_id, 
        models.JobDescription.user_id == user_id
    ).first()
    
    if not db_job:
        return None
    
    update_data = job.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_job, key, value)
    
    db.commit()
    db.refresh(db_job)
    return db_job

def delete_job_description(db: Session, job_id: int, user_id: int):
    db_job = db.query(models.JobDescription).filter(
        models.JobDescription.id == job_id, 
        models.JobDescription.user_id == user_id
    ).first()
    
    if not db_job:
        return False
    
    db.delete(db_job)
    db.commit()
    return True

# Proposal operations
def get_proposal(db: Session, proposal_id: int):
    return db.query(models.Proposal).filter(models.Proposal.id == proposal_id).first()

def get_proposals_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Proposal).join(
        models.Profile, models.Proposal.profile_id == models.Profile.id
    ).filter(
        models.Profile.user_id == user_id
    ).order_by(desc(models.Proposal.created_at)).offset(skip).limit(limit).all()

def create_proposal(db: Session, proposal: schemas.ProposalCreate):
    db_proposal = models.Proposal(
        profile_id=proposal.profile_id,
        job_description_id=proposal.job_description_id,
        headline=proposal.headline,
        body=proposal.body,
        full_text=proposal.full_text
    )
    db.add(db_proposal)
    db.commit()
    db.refresh(db_proposal)
    return db_proposal

def delete_proposal(db: Session, proposal_id: int, user_id: int):
    # We need to join with Profile to check user ownership
    db_proposal = db.query(models.Proposal).join(
        models.Profile, models.Proposal.profile_id == models.Profile.id
    ).filter(
        models.Proposal.id == proposal_id,
        models.Profile.user_id == user_id
    ).first()
    
    if not db_proposal:
        return False
    
    db.delete(db_proposal)
    db.commit()
    return True
