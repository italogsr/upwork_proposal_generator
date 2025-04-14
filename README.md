# Upwork Proposal Generator

A LangGraph-powered tool that automatically generates personalized Upwork proposals based on your profile and job descriptions. This tool helps freelancers create compelling, tailored proposals that address client pain points and highlight relevant skills and experience.

## Quick Start

The fastest way to get started is using Docker:

```bash
# Clone the repository
git clone https://github.com/yourusername/upwork_proposal_generator.git
cd upwork_proposal_generator

# Run the Docker setup script
./docker-run.sh
```

Then access the application at:
- Streamlit Frontend: http://localhost:8501
- Flask Frontend: http://localhost:8502
- API Documentation: http://localhost:8000/docs

For detailed setup instructions, see the [Installation](#installation) section below.

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

You can run the Upwork Proposal Generator either locally or using Docker containers.

### Option 1: Docker Setup (Recommended)

The easiest way to get started is using Docker, which handles all dependencies and configuration automatically.

#### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Groq API key](https://console.groq.com/) for LLM access

#### Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/upwork_proposal_generator.git
   cd upwork_proposal_generator
   ```

2. Run the helper script:
   ```bash
   ./docker-run.sh
   ```

   This script will:
   - Create a `.env` file from the template if it doesn't exist
   - Check if your Groq API key is set
   - Build and start the containers

3. Access the application:
   - API Documentation: http://localhost:8000/docs
   - Streamlit Frontend: http://localhost:8501
   - Flask Frontend: http://localhost:8502

For more detailed Docker instructions, see [DOCKER_README.md](DOCKER_README.md).

### Option 2: Local Setup

#### Prerequisites

- Python 3.9 or higher
- [Groq API key](https://console.groq.com/) for LLM access
- PostgreSQL database (local or remote)

#### Setup

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
   DATABASE_USER=your_database_user
   DATABASE_PASSWORD=your_database_password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   JWT_SECRET_KEY=your_secret_key_for_jwt_tokens
   FLASK_SECRET_KEY=your_secret_key_for_flask
   ```

6. Set up the database:
   ```bash
   # Install PostgreSQL (Ubuntu/Debian)
   sudo apt-get update
   sudo apt-get install postgresql postgresql-contrib

   # Start PostgreSQL service if not already running
   sudo systemctl start postgresql

   # Create the database and user (run as postgres user)
   sudo -u postgres psql -c "CREATE DATABASE upwork_proposal_generator;"
   sudo -u postgres psql -c "CREATE USER your_database_user WITH PASSWORD 'your_database_password';"
   sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE upwork_proposal_generator TO your_database_user;"
   sudo -u postgres psql -d upwork_proposal_generator -c "GRANT ALL ON SCHEMA public TO your_database_user;"

   # Create the database tables
   python db_schema.py
   ```

   Note: If you're using a different operating system, please refer to the [PostgreSQL documentation](https://www.postgresql.org/download/) for installation instructions.

7. Test the database connection:
   ```bash
   # Run the test connection script
   python test_db_connection.py
   ```

   You should see output similar to:
   ```
   Successfully connected to the database!
   PostgreSQL version: PostgreSQL 16.8 (Ubuntu 16.8-0ubuntu0.24.04.1) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0, 64-bit
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
├── docker/               # Docker configuration
│   ├── backend/          # Backend container configuration
│   │   ├── Dockerfile    # Backend container definition
│   │   └── start.sh      # Backend startup script
│   ├── streamlit/        # Streamlit container configuration
│   │   ├── Dockerfile    # Streamlit container definition
│   │   └── start.sh      # Streamlit startup script
│   ├── flask/            # Flask container configuration
│   │   ├── Dockerfile    # Flask container definition
│   │   └── start.sh      # Flask startup script
│   ├── db/               # Database container configuration
│   │   └── init.sql      # Database initialization script
│   └── requirements.txt  # Docker container dependencies
├── database_config.py    # Database connection configuration
├── db_schema.py          # Database schema creation script
├── create_tables.py      # Database tables creation script
├── test_db_connection.py # Script to test database connectivity
├── .env.example          # Example environment variables for local setup
├── .env.docker           # Example environment variables for Docker setup
├── docker-compose.yml    # Docker Compose configuration
├── docker-run.sh         # Helper script for Docker setup
├── DOCKER_README.md      # Docker setup instructions
├── requirements.txt      # Project dependencies
├── run_api.py            # Script to run the API
├── run_frontend.py       # Script to run the Streamlit frontend
└── run_flask_frontend.py # Script to run the Flask frontend
```

## Database Configuration

The application uses a PostgreSQL database for storing user profiles, job descriptions, and generated proposals. For detailed information about the database setup and schema, see [DATABASE_README.md](DATABASE_README.md).

Basic database configuration is defined in `database_config.py`:

```python
# Database connection parameters
DB_CONFIG = {
    'dbname': 'upwork_proposal_generator',
    'user': os.getenv('DATABASE_USER'),
    'password': os.getenv('DATABASE_PASSWORD'),
    'host': os.getenv('DATABASE_HOST', 'localhost'),
    'port': os.getenv('DATABASE_PORT', '5432')
}

# Connection string format for SQLAlchemy
DB_URI = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
```

## Database Schema

The application uses a PostgreSQL database with the following tables:

### Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);
```

### Profiles Table

```sql
CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    skills TEXT[],
    experience INTEGER DEFAULT 0,
    price INTEGER DEFAULT 0,
    description TEXT,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);
```

### Job Descriptions Table

```sql
CREATE TABLE job_descriptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    post_title VARCHAR(255) NOT NULL,
    post_description TEXT NOT NULL,
    post_skills_founded TEXT[],
    skills_asked_expliced TEXT[],
    level_asked VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);
```

### Proposals Table

```sql
CREATE TABLE proposals (
    id SERIAL PRIMARY KEY,
    profile_id INTEGER REFERENCES profiles(id),
    job_description_id INTEGER REFERENCES job_descriptions(id),
    headline TEXT,
    body TEXT,
    full_text TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);
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
  - Stores user profiles with skills, experience, and education
  - Saves job descriptions and requirements
  - Archives generated proposals for future reference
- **psycopg2**: For PostgreSQL database connectivity
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