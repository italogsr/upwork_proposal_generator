from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import logging

def generate_proposal(llm, arguments, job_description, job_post_title):
    class ProposalOutput(BaseModel):
        headline: str = Field(..., description="First line of the proposal that grabs attention")
        body: str = Field(..., description="Main content of the proposal")
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

        Return in this format:
        {
            "headline": "Your attention-grabbing headline",
            "body": "The main content of your proposal",
            "full_text": "The complete proposal text"
        }
        """)
    ]

    try:
        proposal_structured_llm = llm.with_structured_output(ProposalOutput)
        return proposal_structured_llm.invoke(proposal_generation_prompt)
    except Exception as e:
        logging.error(f"Error in structured output: {str(e)}")
        # Return a default structured response with a more helpful message
        return ProposalOutput(
            headline="I Can Deliver Exceptional Results for Your Project",
            body="As an experienced professional, I understand your needs and can deliver high-quality work that meets your requirements. My approach combines technical expertise with attention to detail, ensuring that your project is completed to the highest standards. I'm ready to start immediately and would love to discuss how I can help you achieve your goals.",
            full_text="I Can Deliver Exceptional Results for Your Project\n\nAs an experienced professional, I understand your needs and can deliver high-quality work that meets your requirements. My approach combines technical expertise with attention to detail, ensuring that your project is completed to the highest standards. I'm ready to start immediately and would love to discuss how I can help you achieve your goals."
        )
