from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import logging

def selecting_arguments(llm, profile_headline, profile_summary, protifolio, pain_points, skills_needed):
    class Argument(BaseModel):
        pain_point: str = Field(..., description="The client's pain point or required skill")
        solution: str = Field(..., description="How I can address this need based on my experience")

    class SelectedArguments(BaseModel):
        arguments: List[Argument] = Field(..., description="List of matching arguments between my experience and client needs")

    # Ensure we have at least some skills and pain points to work with
    if not skills_needed or len(skills_needed) == 0:
        skills_needed = ["General expertise in this field", "Professional experience", "Quality work delivery"]

    if not pain_points or len(pain_points) == 0:
        pain_points = ["Needs professional assistance", "Looking for expertise", "Requires quality work"]

    selecting_arguments_prompt = f"""
    Create specific matches between the client's needs and my experience.

    Profile Information:
    Headline: {profile_headline}
    Summary: {profile_summary}
    Portfolio: {protifolio}

    Client Needs:
    Pain Points: {pain_points}
    Required Skills: {skills_needed}

    For each key client need, provide:
    1. The specific pain point or skill needed
    2. How my experience directly addresses it, with concrete examples
    """

    selected_arguments_prompt = [
        ('system', selecting_arguments_prompt),
        ('user', """Return a list of arguments in this format:
        {
            "arguments": [
                {
                    "pain_point": "specific need",
                    "solution": "how I address it with specific example"
                },
                ...
            ]
        }
        Include 3-4 strongest matches.""")
    ]

    try:
        selected_arguments_structured_llm = llm.with_structured_output(SelectedArguments)
        return selected_arguments_structured_llm.invoke(selected_arguments_prompt)
    except Exception as e:
        logging.error(f"Error in structured output: {str(e)}")
        # Return a default structured response
        return SelectedArguments(arguments=[
            Argument(
                pain_point="Professional expertise",
                solution="I bring years of experience and a proven track record of delivering high-quality results."
            ),
            Argument(
                pain_point="Quality work",
                solution="I focus on delivering exceptional quality that exceeds expectations and meets all requirements."
            ),
            Argument(
                pain_point="Timely delivery",
                solution="I understand the importance of deadlines and always ensure on-time delivery of all project milestones."
            )
        ])