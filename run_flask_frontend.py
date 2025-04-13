import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv("FLASK_PORT", "8502"))
    
    # Set environment variables for Flask
    os.environ["FLASK_APP"] = "src.flask_frontend.app"
    os.environ["FLASK_ENV"] = "development"
    
    # Import and run the Flask app
    from src.flask_frontend.app import app
    app.run(host="0.0.0.0", port=port, debug=True)
