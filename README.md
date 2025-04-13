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
- **Streamlit Frontend**: User-friendly interface for inputting profile and job information
  - Intuitive forms for profile and job details
  - Real-time proposal generation
  - Copy-to-clipboard functionality

## Installation

### Prerequisites

- Python 3.9 or higher
- [Groq API key](https://console.groq.com/) for LLM access

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

5. Add your Groq API key to the `.env` file:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

   You can also configure other settings in the `.env` file:
   ```
   API_URL=http://localhost:8000  # URL for the frontend to connect to
   API_PORT=8000                  # Port for the API server
   STREAMLIT_PORT=8501            # Port for the Streamlit frontend
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

### Using the Application

1. **Profile Setup**:
   - Enter your name, skills, experience, and profile description
   - Your profile information will be saved in the session

2. **Job Description**:
   - Enter the job title and full job description
   - Optionally specify skills and experience level mentioned in the job

3. **Generate Proposal**:
   - Click the "Generate Proposal" button to create your personalized proposal
   - The system will analyze the job, extract skills and pain points, and match them to your profile
   - A complete proposal with headline and body will be generated

4. **Use Your Proposal**:
   - Review the generated proposal
   - Copy the full text to use in your Upwork application

## API Endpoints

- `GET /`: Welcome message
- `GET /health`: Health check endpoint
- `POST /generate-proposal`: Generate a proposal based on profile and job description

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
│   │   └── models.py    # API data models
│   ├── frontend/         # Streamlit frontend
│   │   └── app.py       # Streamlit application
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
└── run_frontend.py       # Script to run the frontend
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
- **Streamlit**: For building the user interface
- **Pydantic**: For data validation and settings management

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
- [Streamlit](https://streamlit.io/) for the frontend framework