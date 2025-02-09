import os
import logging
from pathlib import Path
from functools import wraps
from datetime import datetime
import traceback
import chainlit as cl
from dotenv import load_dotenv

class CommonUtils:

    @staticmethod
    def async_error_handler(func):
        """Decorator for handling errors in async functions."""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                error_msg = f"Error in {func.__name__}: {str(e)}"
                logging.error(error_msg, extra={
                    'traceback': traceback.format_exc()
                })
                return await cl.Message(
                    content=f"❌ Error: {str(e)}"
                ).send()
        return wrapper

    @staticmethod
    def load_openai_key():
        """Retrieve OpenAI API key from environment variables or .env file."""
        # Try to load from .env file if it exists
        env_path = Path('.env')
        if env_path.exists():
            load_dotenv()
        
        # Get key from environment variable
        openai_key = os.getenv('OPENAI_API_KEY')
        
        if not openai_key:
            raise ValueError(
                "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable "
                "or add it to a .env file in the project root directory."
            )
        
        return openai_key
