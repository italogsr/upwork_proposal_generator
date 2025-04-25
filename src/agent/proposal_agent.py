from typing import Dict, List, Annotated, TypedDict, Literal, Optional
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from pydantic import BaseModel

from src.nodes.skill_extractor import get_skills
from src.nodes.pain_points_extractor import get_pain_points
from src.nodes.arguments_selector import selecting_arguments
from src.nodes.proposal_generator import generate_proposal
from src.states.states import InfoProfile, Jobdescription, ProposalState
import logging
from dotenv import load_dotenv
import os
load_dotenv()

# Define the state for the graph
class AgentState(TypedDict):
    profile: InfoProfile
    job: Jobdescription
    skills: List[str]
    pain_points: List[str]
    arguments: Dict
    proposal: ProposalState

# Define the nodes for the graph
def extract_skills(state: AgentState, llm) -> AgentState:
    """Extract skills from job description"""
    skills_result = get_skills(llm, state["job"].post_description, state["job"].post_title)
    return {"skills": skills_result.skills}

def extract_pain_points(state: AgentState, llm) -> AgentState:
    """Extract pain points from job description"""
    pain_points_result = get_pain_points(llm, state["job"].post_description, state["job"].post_title)
    return {"pain_points": pain_points_result.pain_points}

def select_arguments(state: AgentState, llm) -> AgentState:
    """Select arguments based on profile and job requirements"""
    arguments_result = selecting_arguments(
        llm,
        state["profile"].description.split("\n")[0],  # Use first line as headline
        state["profile"].description,
        "",  # Portfolio is empty for now
        state["pain_points"],
        state["skills"]
    )
    return {"arguments": arguments_result.arguments}

def generate_proposal_text(state: AgentState, llm) -> AgentState:
    """Generate proposal text"""
    proposal_result = generate_proposal(
        llm,
        state["arguments"],
        state["job"].post_description,
        state["job"].post_title
    )
    proposal_state = ProposalState(
        full_text=proposal_result.full_text
    )
    
    return {"proposal": proposal_state}

def create_proposal_agent(llm):
    """Create a proposal agent using LangGraph"""
    # Create a new graph
    workflow = StateGraph(AgentState)
    
    # Add nodes to the graph
    workflow.add_node("extract_skills", lambda state: extract_skills(state, llm))
    workflow.add_node("extract_pain_points", lambda state: extract_pain_points(state, llm))
    workflow.add_node("select_arguments", lambda state: select_arguments(state, llm))
    workflow.add_node("generate_proposal", lambda state: generate_proposal_text(state, llm))
    
    # Define the edges
    workflow.add_edge("extract_skills", "extract_pain_points")
    workflow.add_edge("extract_pain_points", "select_arguments")
    workflow.add_edge("select_arguments", "generate_proposal")
    workflow.add_edge("generate_proposal", END)
    
    # Set the entry point
    workflow.set_entry_point("extract_skills")
    
    # Compile the graph
    return workflow.compile()

def initialize_llm(api_key, model=os.environ["GROQ_MODEL"]):
    """Initialize the LLM"""
    return ChatGroq(
        api_key=api_key,
        model=model,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )

def run_proposal_agent(profile: InfoProfile, job: Jobdescription, client_id: Optional[str] = None, model=os.environ["GROQ_MODEL"]):
    """Run the proposal agent"""
    # Initialize the LLM
    llm = initialize_llm(os.environ["GROQ_API_KEY"], model)
    
    # Create the agent
    agent = create_proposal_agent(llm)
    
    # Initialize the state
    initial_state = AgentState(
        profile=profile,
        job=job,
        skills=[],
        pain_points=[],
        arguments={},
        proposal=None
    )
    
    # Run the agent
    result = agent.invoke(initial_state)
    if client_id:
        logging.info(f"Proposal generated for client ID: {client_id}")
    
    return result["proposal"]
