from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any

def selecting_arguments(llm, profile_headline, profile_summary, protifolio, pain_points, skills_needed):
    class Argument(BaseModel):
        pain_point: str = Field(..., description="The client's pain point or required skill")
        solution: str = Field(..., description="How I can address this need based on my experience")

    class SelectedArguments(BaseModel):
        arguments: List[Argument] = Field(..., description="List of matching arguments between my experience and client needs")

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
        print(f"Error in structured output: {str(e)}")
        # Return a default structured response
        return SelectedArguments(arguments=[
            Argument(
                pain_point="Error processing response",
                solution="Please try running the query again"
            )
        ])