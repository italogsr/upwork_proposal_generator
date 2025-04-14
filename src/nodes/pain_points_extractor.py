from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import logging


def get_pain_points(llm, job_description, job_post_tile):
    class PainPointsFormater(BaseModel):
        pain_points: List[str] = []

    client_motivations_prompt= f"""
    Extract the client motivations from the following upwork job description:
    - Considere why the client is looking for a freelancer
    - Identify the main pain points that the client is facing that lead him to post a job.
    - Consider not only the pain points mentioned in the job description, but also the underlying issues that the client is facing.
    - If no specific pain points are mentioned, infer general motivations based on the job type.
    - Always return at least a few general motivations even if none are explicitly mentioned.

    <job_title>
    {job_post_tile}
    </job_title>

    <job_description>
    {job_description}
    </job_description>
    """

    pain_prompt = [
        ('system', client_motivations_prompt),
        ('user', "return a python list of the pain points")
    ]

    try:
        pain_points_structured_llm = llm.with_structured_output(PainPointsFormater)
        pain_points = pain_points_structured_llm.invoke(pain_prompt)
        return pain_points
    except Exception as e:
        logging.error(f"Error extracting pain points: {str(e)}")
        # Return a default response with generic pain points
        return PainPointsFormater(pain_points=["Needs professional assistance", "Looking for expertise", "Requires quality work"])