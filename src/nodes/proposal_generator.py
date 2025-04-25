from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import logging

def generate_proposal(llm, arguments, job_description, job_post_title):
    class ProposalOutput(BaseModel):
        full_text: str = Field(..., description="Complete proposal text")

    proposal_prompt = f"""
    You are an assistant specialized in crafting freelance proposals..Create a compelling Upwork proposal based on the following information:

    Job Title: {job_post_title}

    Job Description:
    {job_description}

    Key Arguments to Include:
    {arguments}

    When given the details below, produce a clear, concise, and persuasive proposal following this structure:

    1. **Personalized Greeting**  
    2. **Quick Hook** (show you understand the client’s need)  
    3. **Relevant Experience Highlight** (1–2 sentences with results or company names)  
    4. **Proposed Solution Summary** (2–3 sentences on tools and benefits)  
    5. **Key Achievements in Bullets** (2–3 items with metrics/impact)  
    6. **Social Proof / Testimonials** (1–2 short quotes prefaced by ✅)  
    7. **Low-Barrier Call to Action** (what you need to get started)  
    8. **Warm Sign-Off**  

    **Input format** (replace bracketed sections with real content):

    - Client name: [Name]  
    - Project description: [Text from the job post]  
    - Your relevant experience: [Summary, company, metrics]  
    - Approach/solution: [Tools and benefits]  
    - Past results (bullets):  
    - [e.g., “Processed X transactions/day with <Y ms latency”]  
    - [e.g., “Reduced error rate by Z%”]  
    - Testimonials (optional):  
    - ✅ “[Short quote]” – [Client Name]  
    - Information needed for CTA: [e.g., “current tech stack,” “data volume”]  

    **Example final prompt:**

    “You are an expert in Upwork proposals. Generate a proposal based on the information below:

    Client name: Angelika  
    Project description: Anomaly detection on real-time data streams using Google Colab  
    Your relevant experience: Built an anomaly-detection model for Heineken Brazil, processing 10,000 transactions/day via a REST API  
    Approach/solution: Develop the model in Google Colab, deploy to a scalable real-time environment with low latency and high accuracy  
    Past results:
    - Processed 2M records/month with <100 ms latency  
    - Reduced error rate by 35%  
    Testimonials:
    ✅ “Italo is one of the most impactful professionals I’ve worked with.” – Igor Aboim  
    Information needed for CTA: Current tech stack and data volume

    Follow the structure above and deliver a proposal of ~150–200 words.”```

    The output shold be a complete proposal ready to send to the client.
    Dont Make up information. Only use the information provided.

    Remove subtitles. Return only the proposal.
    """

    proposal_generation_prompt = [
        ('system', proposal_prompt),
        ('user', """Generate a proposal that wins the client's attention and convinces them to hire.""")
    ]

    try:
        proposal_structured_llm = llm.with_structured_output(ProposalOutput)
        return proposal_structured_llm.invoke(proposal_generation_prompt)
    except Exception as e:
        logging.error(f"Error in structured output: {str(e)}")
        return None
