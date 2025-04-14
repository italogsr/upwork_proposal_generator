from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import logging

def get_skills(llm, job_description, job_post_tile):
    class SkillsFormater(BaseModel):
        skills: List[str] = []

    skill_stractor_prompt = f"""
    Bellow is a Upwork job description.
    Extract Skills needed to perform the job from the following job description.
    If no specific skills are mentioned, infer general skills that would be needed for this type of job.
    Always return at least a few general skills even if none are explicitly mentioned.

    <job_title>
    {job_post_tile}
    </job_title>

    <job_description>
    {job_description}
    </job_description>
    """
    skill_prompt = [
        ('system', skill_stractor_prompt),
        ('user', "return a python list of the skills needed")
    ]

    try:
        skills_structured_llm = llm.with_structured_output(SkillsFormater)
        skills_needed = skills_structured_llm.invoke(skill_prompt)
        return skills_needed
    except Exception as e:
        logging.error(f"Error extracting skills: {str(e)}")
        # Return a default response with empty skills list
        return SkillsFormater(skills=[])