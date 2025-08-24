import os
import sys
from dotenv import load_dotenv

# Add project root (one level above) to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables from .env
load_dotenv()