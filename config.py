import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_api_key_here":
        print("WARNING: GEMINI_API_KEY is not set or using default value in .env file.")

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    
# Map environments
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
