import streamlit as st
import requests
import json
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Upwork Proposal Generator",
    page_icon="📝",
    layout="wide",
)

# Define API URL
API_URL = os.getenv("API_URL", "http://localhost:8000")

def generate_proposal(profile_data: Dict, job_data: Dict) -> Dict:
    """Generate a proposal using the API"""
    try:
        response = requests.post(
            f"{API_URL}/generate-proposal",
            json={
                "profile": profile_data,
                "job": job_data
            },
            timeout=180  # Increase timeout to 3 minutes
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 504:
            st.error("Request timed out. The server took too long to respond.")
        else:
            st.error(f"Error {response.status_code}: {response.text}")
        return None
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API server. Please ensure it's running.")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# App title
st.title("Upwork Proposal Generator")
st.markdown("Generate compelling Upwork proposals based on your profile and job descriptions.")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Profile", "Job Description", "Generated Proposal"])

# Profile tab
with tab1:
    st.header("Your Profile")
    
    # Profile form
    with st.form("profile_form"):
        name = st.text_input("Name", value="", help="Your full name")
        
        # Skills
        skills_input = st.text_area(
            "Skills (one per line)",
            value="",
            help="Enter your skills, one per line"
        )
        
        experience = st.number_input(
            "Years of Experience",
            min_value=0,
            max_value=50,
            value=5,
            help="Your years of professional experience"
        )
        
        price = st.number_input(
            "Hourly Rate (USD)",
            min_value=0,
            max_value=500,
            value=50,
            help="Your hourly rate in USD"
        )
        
        profile_description = st.text_area(
            "Profile Description",
            value="",
            height=300,
            help="Your Upwork profile description or summary"
        )
        
        profile_submit = st.form_submit_button("Save Profile")
    
    if profile_submit:
        # Process skills
        skills_list = [skill.strip() for skill in skills_input.split("\n") if skill.strip()]
        
        # Save profile to session state
        st.session_state.profile = {
            "name": name,
            "skills": skills_list,
            "experience": experience,
            "price": price,
            "description": profile_description
        }
        
        st.success("Profile saved successfully!")

# Job Description tab
with tab2:
    st.header("Job Description")
    
    # Job form
    with st.form("job_form"):
        job_title = st.text_input("Job Title", value="", help="The title of the job post")
        
        job_description = st.text_area(
            "Job Description",
            value="",
            height=300,
            help="The full job description from Upwork"
        )
        
        # Skills asked
        skills_asked_input = st.text_area(
            "Skills Asked (one per line, optional)",
            value="",
            help="Skills explicitly mentioned in the job post, one per line"
        )
        
        level_asked = st.selectbox(
            "Experience Level",
            options=["", "Entry Level", "Intermediate", "Expert"],
            help="Experience level mentioned in the job post"
        )
        
        job_submit = st.form_submit_button("Save Job Description")
    
    if job_submit:
        # Process skills asked
        skills_asked_list = [skill.strip() for skill in skills_asked_input.split("\n") if skill.strip()]
        
        # Save job to session state
        st.session_state.job = {
            "post_title": job_title,
            "post_description": job_description,
            "skills_asked_expliced": skills_asked_list if skills_asked_list else None,
            "level_asked": level_asked if level_asked else None
        }
        
        st.success("Job description saved successfully!")

# Generated Proposal tab
with tab3:
    st.header("Generated Proposal")
    
    # Check if profile and job are in session state
    if 'profile' not in st.session_state or 'job' not in st.session_state:
        st.warning("Please fill out your profile and job description first.")
    else:
        if st.button("Generate Proposal"):
            with st.spinner("Generating proposal..."):
                # Generate proposal
                proposal = generate_proposal(st.session_state.profile, st.session_state.job)
                
                if proposal:
                    # Save proposal to session state
                    st.session_state.proposal = proposal
        
        # Display proposal if available
        if 'proposal' in st.session_state:
            st.subheader("Headline")
            st.write(st.session_state.proposal["headline"])
            
            st.subheader("Body")
            st.write(st.session_state.proposal["body"])
            
            st.subheader("Full Proposal")
            full_text = st.session_state.proposal["full_text"]
            st.text_area("Copy this text", value=full_text, height=300)
            
            # Copy button
            if st.button("Copy to Clipboard"):
                st.code(full_text)
                st.success("Copied to clipboard! (Use Ctrl+C to copy the text above)")
