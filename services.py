import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_services():
    """
    Returns a dictionary of services, such as API keys and configuration data.
    """
    services = {
        "openai_key": os.getenv("OPENAI_API_KEY"),  # Load OpenAI API key from .env
        # Add other services here as needed
        # Example: "gmail_token": os.getenv("GMAIL_API_TOKEN"),
    }

    # Ensure the required services are available
    if not services.get("openai_key"):
        raise ValueError("OpenAI API key is missing in environment variables.")
    
    return services



