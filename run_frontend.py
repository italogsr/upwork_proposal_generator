import streamlit.web.cli as stcli
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv("STREAMLIT_PORT", "8501"))
    
    # Set environment variables for Streamlit
    os.environ["STREAMLIT_SERVER_PORT"] = str(port)
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    
    # Run the Streamlit app
    sys.argv = ["streamlit", "run", "src/frontend/app.py"]
    sys.exit(stcli.main())
