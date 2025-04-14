from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from dotenv import load_dotenv
import requests
from typing import Dict
from markupsafe import Markup  # Changed from jinja2 import Markup

load_dotenv()

app = Flask(__name__)
# Set a strong secret key for session management
app.secret_key = os.getenv('FLASK_SECRET_KEY')
# Set session type to filesystem
app.config['SESSION_TYPE'] = 'filesystem'

# Add nl2br filter
@app.template_filter('nl2br')
def nl2br_filter(text):
    if not text:
        return ""
    return Markup(text.replace('\n', '<br>'))

# Define API URL
API_URL = os.getenv("API_URL", "http://localhost:8000")

def generate_proposal(profile_data: Dict, job_data: Dict) -> Dict:
    """Generate a proposal using the API"""
    try:
        # Debug prints
        print("Session contents:", dict(session))
        print("Access token exists:", 'access_token' in session)
        
        # Check if user is authenticated
        if not session.get('access_token'):
            flash("Please log in to generate proposals.", "error")
            return None

        # Debug print
        print(f"Using token: {session['access_token'][:20]}...")
        
        headers = {
            "Authorization": f"Bearer {session['access_token']}",
            "Content-Type": "application/json"
        }
        
        # Debug print
        print("Request headers:", headers)
        print("Request data:", {"profile": profile_data, "job": job_data})

        response = requests.post(
            f"{API_URL}/generate-proposal",
            json={
                "profile": profile_data,
                "job": job_data
            },
            headers=headers,
            timeout=180  # Increase timeout to 3 minutes
        )

        # Debug print
        print("Response status:", response.status_code)
        print("Response body:", response.text)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            flash("Your session has expired. Please log in again.", "error")
            session.clear()  # Clear the invalid session
            return None
        elif response.status_code == 504:
            flash("Request timed out. The server took too long to respond.", "error")
        else:
            flash(f"Error {response.status_code}: {response.text}", "error")
        return None
    except requests.exceptions.Timeout:
        flash("Request timed out. Please try again.", "error")
        return None
    except requests.exceptions.ConnectionError:
        flash("Could not connect to the API server. Please ensure it's running.", "error")
        return None
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        # Process skills
        skills_input = request.form.get('skills', '')
        skills_list = [skill.strip() for skill in skills_input.split("\n") if skill.strip()]

        # Save profile to session
        session['profile'] = {
            "name": request.form.get('name', ''),
            "skills": skills_list,
            "experience": int(request.form.get('experience', 5)),
            "price": int(request.form.get('price', 50)),
            "description": request.form.get('description', '')
        }

        flash("Profile saved successfully!", "success")
        return redirect(url_for('profile'))

    # For GET request, display the form with existing data if available
    profile_data = session.get('profile', {
        "name": "",
        "skills": [],
        "experience": 5,
        "price": 50,
        "description": ""
    })

    return render_template('profile.html', profile=profile_data)

@app.route('/job', methods=['GET', 'POST'])
def job():
    if request.method == 'POST':
        # Process skills asked
        skills_asked_input = request.form.get('skills_asked', '')
        skills_asked_list = [skill.strip() for skill in skills_asked_input.split("\n") if skill.strip()]

        # Save job to session
        session['job'] = {
            "post_title": request.form.get('job_title', ''),
            "post_description": request.form.get('job_description', ''),
            "skills_asked_expliced": skills_asked_list if skills_asked_list else None,
            "level_asked": request.form.get('level_asked', '') or None
        }

        flash("Job description saved successfully!", "success")
        return redirect(url_for('job'))

    # For GET request, display the form with existing data if available
    job_data = session.get('job', {
        "post_title": "",
        "post_description": "",
        "skills_asked_expliced": [],
        "level_asked": ""
    })

    return render_template('job.html', job=job_data)

@app.route('/proposal', methods=['GET', 'POST'])
def proposal():
    # Check if user is authenticated
    if not session.get('is_authenticated'):
        flash("Please log in to generate proposals.", "warning")
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Check if profile and job are in session
        if 'profile' not in session or 'job' not in session:
            flash("Please fill out your profile and job description first.", "warning")
            return redirect(url_for('proposal'))

        # Generate proposal
        proposal_data = generate_proposal(session['profile'], session['job'])

        if proposal_data:
            # Save proposal to session
            session['proposal'] = proposal_data

    # For GET request, display the proposal if available
    return render_template('proposal.html',
                          has_profile='profile' in session,
                          has_job='job' in session,
                          proposal=session.get('proposal'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

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
                token_data = response.json()
                session['access_token'] = token_data['access_token']
                session['is_authenticated'] = True
                # Add debug print
                print(f"Token stored in session: {session['access_token'][:20]}...")
                flash("Login successful!", "success")
                return redirect(url_for('index'))
            else:
                flash(f"Login failed: {response.text}", "error")
        except Exception as e:
            flash(f"Error during login: {str(e)}", "error")

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

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
                flash("Registration successful! Please log in.", "success")
                return redirect(url_for('login'))
            else:
                flash(f"Registration failed: {response.text}", "error")
        except Exception as e:
            flash(f"Error during registration: {str(e)}", "error")

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv("FLASK_PORT", "8502")))
