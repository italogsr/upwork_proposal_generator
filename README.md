# Upwork Proposal Generator

A LangGraph-powered tool that automatically generates personalized Upwork proposals based on your profile and job descriptions. This tool helps freelancers create compelling, tailored proposals that address client pain points and highlight relevant skills and experience.

## Features

- **LangGraph Agent**: Intelligent proposal generation using a multi-step agent workflow
  - Extracts skills from job descriptions
  - Identifies client pain points and motivations
  - Matches your experience to client needs
  - Generates compelling headlines and proposal content
- **API**: FastAPI implementation for interacting with the proposal generator
  - RESTful endpoints for proposal generation
  - Structured request/response models
  - Error handling and validation
  - User authentication with JWT tokens
  - Database integration for storing profiles, jobs, and proposals
- **Streamlit Frontend**: User-friendly interface for inputting profile and job information
  - Intuitive forms for profile and job details
  - Real-time proposal generation
  - Copy-to-clipboard functionality
  - User authentication
  - Save and load profiles, job descriptions, and proposals
- **Flask Frontend**: Alternative web interface with the same functionality
  - Bootstrap-based responsive design
  - Modern UI with tabs and cards
  - Session-based data storage
  - Authentication integration with the API
- **Database**: PostgreSQL database for persistent storage
  - Store user profiles and preferences
  - Save job descriptions for future reference
  - Archive generated proposals
  - User account management

## Installation

### Prerequisites

- Python 3.9 or higher
- [Groq API key](https://console.groq.com/) for LLM access
- PostgreSQL database (local or remote)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/upwork_proposal_generator.git
   cd upwork_proposal_generator
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on the `.env.example` file:
   ```bash
   cp .env.example .env
   ```

5. Add your Groq API key and database configuration to the `.env` file:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   DATABASE_URL=your_postgresql_database_url_here
   SECRET_KEY=your_secret_key_for_jwt_tokens
   ```

   You can also configure other settings in the `.env` file:
   ```
   API_URL=http://localhost:8000  # URL for the frontend to connect to
   API_PORT=8000                  # Port for the API server
   STREAMLIT_PORT=8501            # Port for the Streamlit frontend
   FLASK_PORT=8502                # Port for the Flask frontend
   ```

6. Set up the database:
   ```bash
   # Create the database (if not already created)
   createdb upwork_proposal_generator

   # Run the database migrations
   python -m src.db.migrations.create_tables
   ```

## Usage

### Running the API

Start the FastAPI server:

```bash
python run_api.py
```

The API will be available at http://localhost:8000

You can access the API documentation at http://localhost:8000/docs

### Running the Streamlit Frontend

Start the Streamlit application:

```bash
python run_frontend.py
```

The frontend will be available at http://localhost:8501

### Running the Flask Frontend

Start the Flask application:

```bash
python run_flask_frontend.py
```

The Flask frontend will be available at http://localhost:8502

### Using the Application

1. **Authentication**:
   - Register for a new account or log in with your existing credentials
   - Your authentication token will be stored in the session

2. **Profile Setup**:
   - Enter your name, skills, experience, and profile description
   - Save your profile to the database for future use
   - Set a default profile for quick access
   - Load and edit existing profiles

3. **Job Description**:
   - Enter the job title and full job description
   - Optionally specify skills and experience level mentioned in the job
   - Save job descriptions to the database for future reference
   - Load and edit existing job descriptions

4. **Generate Proposal**:
   - Click the "Generate Proposal" button to create your personalized proposal
   - The system will analyze the job, extract skills and pain points, and match them to your profile
   - A complete proposal with headline and body will be generated
   - Save the generated proposal to the database

5. **Use Your Proposal**:
   - Review the generated proposal
   - Copy the full text to use in your Upwork application
   - Access previously generated proposals from the History tab

## API Endpoints

### General Endpoints
- `GET /`: Welcome message
- `GET /health`: Health check endpoint

### Authentication Endpoints
- `POST /token`: Get JWT access token (login)
- `POST /users/`: Create a new user (register)

### Profile Endpoints
- `GET /profiles/`: Get all profiles for the current user
- `GET /profiles/default`: Get the default profile for the current user
- `POST /profiles/`: Create a new profile
- `PUT /profiles/{profile_id}`: Update an existing profile
- `DELETE /profiles/{profile_id}`: Delete a profile

### Job Description Endpoints
- `GET /jobs/`: Get all job descriptions for the current user
- `POST /jobs/`: Create a new job description
- `PUT /jobs/{job_id}`: Update an existing job description
- `DELETE /jobs/{job_id}`: Delete a job description

### Proposal Endpoints
- `GET /proposals/`: Get all proposals for the current user
- `POST /generate-proposal`: Generate a proposal based on profile and job description
- `DELETE /proposals/{proposal_id}`: Delete a proposal

### Request Format for `/generate-proposal`

```json
{
  "profile": {
    "name": "Your Name",
    "skills": ["Skill 1", "Skill 2"],
    "experience": 5,
    "price": 50,
    "description": "Your profile description/summary"
  },
  "job": {
    "post_title": "Job Title",
    "post_description": "Full job description",
    "skills_asked_expliced": ["Required Skill 1", "Required Skill 2"],
    "level_asked": "Expert"
  }
}
```

### Response Format

```json
{
  "headline": "Attention-grabbing headline",
  "body": "Main content of the proposal",
  "full_text": "Complete proposal text"
}
```

## Project Structure

```
├── src/
│   ├── agent/            # LangGraph agent implementation
│   │   └── proposal_agent.py  # Main agent workflow
│   ├── api/              # FastAPI implementation
│   │   ├── main.py      # API endpoints
│   │   ├── models.py    # API data models
│   │   └── auth.py      # Authentication utilities
│   ├── db/               # Database components
│   │   ├── database.py  # Database connection
│   │   ├── models.py    # SQLAlchemy ORM models
│   │   ├── schemas.py   # Pydantic schemas
│   │   ├── crud.py      # Database operations
│   │   └── migrations/  # Database migrations
│   ├── frontend/         # Streamlit frontend
│   │   ├── app.py       # Streamlit application
│   │   └── auth.py      # Authentication utilities for frontend
│   ├── flask_frontend/   # Flask frontend (alternative UI)
│   │   ├── app.py       # Flask application
│   │   ├── templates/   # HTML templates
│   │   └── static/      # CSS, JS, and other static files
│   ├── nodes/            # Agent nodes
│   │   ├── arguments_selector.py  # Match profile to job needs
│   │   ├── pain_points_extractor.py  # Extract client pain points
│   │   ├── proposal_generator.py  # Generate proposal text
│   │   └── skill_extractor.py  # Extract required skills
│   └── states/           # State definitions
│       └── states.py     # Pydantic models for state
├── .env.example          # Example environment variables
├── requirements.txt      # Project dependencies
├── run_api.py            # Script to run the API
├── run_frontend.py       # Script to run the Streamlit frontend
└── run_flask_frontend.py # Script to run the Flask frontend
```

## How It Works

### LangGraph Agent Workflow

1. **Skill Extraction**: The agent analyzes the job description to identify required skills and expertise.

2. **Pain Point Identification**: The agent identifies the client's pain points, challenges, and underlying motivations.

3. **Argument Selection**: The agent matches your profile strengths to the client's needs, creating compelling arguments.

4. **Proposal Generation**: The agent crafts a complete proposal with an attention-grabbing headline and persuasive body text.

### Technologies Used

- **LangGraph**: For creating the multi-step agent workflow
- **Groq LLM**: For natural language processing and text generation
- **FastAPI**: For creating the RESTful API
- **Streamlit**: For building the primary user interface
- **Flask**: For the alternative web interface
- **Bootstrap**: For responsive UI design in the Flask frontend
- **Pydantic**: For data validation and settings management
- **SQLAlchemy**: For ORM and database operations
- **PostgreSQL**: For persistent data storage
- **JWT**: For secure authentication

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT

## Acknowledgments

- [LangGraph](https://github.com/langchain-ai/langgraph) for the agent framework
- [Groq](https://groq.com/) for the LLM API
- [FastAPI](https://fastapi.tiangolo.com/) for the API framework
- [Streamlit](https://streamlit.io/) for the primary frontend framework
- [Flask](https://flask.palletsprojects.com/) for the alternative frontend framework
- [Bootstrap](https://getbootstrap.com/) for the Flask frontend UI components