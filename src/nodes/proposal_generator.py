from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import logging

def generate_proposal(llm, arguments, job_description, job_post_title):
    class ProposalOutput(BaseModel):
        full_text: str = Field(..., description="Complete proposal text")

    proposal_prompt = f"""
    Create a compelling Upwork proposal based on the following information:

    Job Title: {job_post_title}

    Job Description:
    {job_description}

    Key Arguments to Include:
    {arguments}

    Your proposal should:
    1. Start with an attention-grabbing headline that addresses the client's main pain point
    2. Include a personalized introduction that shows you understand their needs
    3. Present 3-4 specific ways your experience addresses their requirements
    4. Include concrete examples and results from your past work
    5. End with a clear call to action
    6. Be professional, confident, and conversational in tone
    7. Be between 200-300 words total
    """

    proposal_generation_prompt = [
        ('system', proposal_prompt),
        ('user', """Generate a proposal with:
        1. A compelling headline
        2. A well-structured body
        3. The full text (headline + body)
        """)
    ]

    try:
        proposal_structured_llm = llm.with_structured_output(ProposalOutput)
        return proposal_structured_llm.invoke(proposal_generation_prompt)
    except Exception as e:
        logging.error(f"Error in structured output: {str(e)}")
        return None
