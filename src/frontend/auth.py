import streamlit as st
import requests
import json
from typing import Dict, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define API URL
API_URL = os.getenv("API_URL", "http://localhost:8000")

def login(email: str, password: str) -> Optional[Dict]:
    """Login to the API and get an access token"""
    try:
        response = requests.post(
            f"{API_URL}/token",
            data={
                "username": email,  # OAuth2 uses username field
                "password": password
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Login failed: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error during login: {str(e)}")
        return None

def register(email: str, password: str) -> bool:
    """Register a new user"""
    try:
        response = requests.post(
            f"{API_URL}/users/",
            json={
                "email": email,
                "password": password
            },
            timeout=10
        )
        
        if response.status_code == 200:
            return True
        else:
            st.error(f"Registration failed: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error during registration: {str(e)}")
        return False

def get_profiles(token: str) -> Optional[list]:
    """Get user profiles from the API"""
    try:
        response = requests.get(
            f"{API_URL}/profiles/",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get profiles: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error getting profiles: {str(e)}")
        return None

def get_default_profile(token: str) -> Optional[Dict]:
    """Get the default profile from the API"""
    try:
        response = requests.get(
            f"{API_URL}/profiles/default",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            # No default profile found, which is okay
            return None
        else:
            st.error(f"Failed to get default profile: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error getting default profile: {str(e)}")
        return None

def get_job_descriptions(token: str) -> Optional[list]:
    """Get user job descriptions from the API"""
    try:
        response = requests.get(
            f"{API_URL}/jobs/",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get job descriptions: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error getting job descriptions: {str(e)}")
        return None

def get_proposals(token: str) -> Optional[list]:
    """Get user proposals from the API"""
    try:
        response = requests.get(
            f"{API_URL}/proposals/",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get proposals: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error getting proposals: {str(e)}")
        return None

def create_profile(token: str, profile_data: Dict) -> Optional[Dict]:
    """Create a new profile"""
    try:
        response = requests.post(
            f"{API_URL}/profiles/",
            json=profile_data,
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to create profile: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error creating profile: {str(e)}")
        return None

def create_job_description(token: str, job_data: Dict) -> Optional[Dict]:
    """Create a new job description"""
    try:
        response = requests.post(
            f"{API_URL}/jobs/",
            json=job_data,
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to create job description: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error creating job description: {str(e)}")
        return None

def delete_profile(token: str, profile_id: int) -> bool:
    """Delete a profile"""
    try:
        response = requests.delete(
            f"{API_URL}/profiles/{profile_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        
        if response.status_code == 200:
            return True
        else:
            st.error(f"Failed to delete profile: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error deleting profile: {str(e)}")
        return False

def delete_job_description(token: str, job_id: int) -> bool:
    """Delete a job description"""
    try:
        response = requests.delete(
            f"{API_URL}/jobs/{job_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        
        if response.status_code == 200:
            return True
        else:
            st.error(f"Failed to delete job description: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error deleting job description: {str(e)}")
        return False

def delete_proposal(token: str, proposal_id: int) -> bool:
    """Delete a proposal"""
    try:
        response = requests.delete(
            f"{API_URL}/proposals/{proposal_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        
        if response.status_code == 200:
            return True
        else:
            st.error(f"Failed to delete proposal: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error deleting proposal: {str(e)}")
        return False
