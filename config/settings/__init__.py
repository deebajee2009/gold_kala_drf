
import os
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()


env = os.getenv('DJANGO_ENV', 'development')  # Default to 'development' if not set

if env == 'development':
    from .development import *
