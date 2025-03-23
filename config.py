import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Key and Constants
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
MAX_ARTICLES = 10
LOG_FILE = "logs/app.log"
