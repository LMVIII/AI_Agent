import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pytz

# Scopes required by Gmail API (add more if needed)
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.settings.basic'
]

STATE_TIMEZONE_MAPPING = {
    "Alabama": "America/Chicago", "Alaska": "America/Anchorage", "Arizona": "America/Phoenix",
    "Arkansas": "America/Chicago", "California": "America/Los_Angeles", "Colorado": "America/Denver",
    "Connecticut": "America/New_York", "Delaware": "America/New_York", "Florida": "America/New_York",
    "Georgia": "America/New_York", "Hawaii": "Pacific/Honolulu", "Idaho": "America/Boise",
    "Illinois": "America/Chicago", "Indiana": "America/Indiana/Indianapolis", "Iowa": "America/Chicago",
    "Kansas": "America/Chicago", "Kentucky": "America/New_York", "Louisiana": "America/Chicago",
    "Maine": "America/New_York", "Maryland": "America/New_York", "Massachusetts": "America/New_York",
    "Michigan": "America/Detroit", "Minnesota": "America/Chicago", "Mississippi": "America/Chicago",
    "Missouri": "America/Chicago", "Montana": "America/Denver", "Nebraska": "America/Chicago",
    "Nevada": "America/Los_Angeles", "New Hampshire": "America/New_York", "New Jersey": "America/New_York",
    "New Mexico": "America/Denver", "New York": "America/New_York", "North Carolina": "America/New_York",
    "North Dakota": "America/Chicago", "Ohio": "America/New_York", "Oklahoma": "America/Chicago",
    "Oregon": "America/Los_Angeles", "Pennsylvania": "America/New_York", "Rhode Island": "America/New_York",
    "South Carolina": "America/New_York", "South Dakota": "America/Chicago", "Tennessee": "America/Chicago",
    "Texas": "America/Chicago", "Utah": "America/Denver", "Vermont": "America/New_York",
    "Virginia": "America/New_York", "Washington": "America/Los_Angeles", "West Virginia": "America/New_York",
    "Wisconsin": "America/Chicago", "Wyoming": "America/Denver"
}

def format_time_to_timezone(utc_time, timezone_name):
    """
    Convert a UTC datetime object to a specific timezone.
    """
    try:
        tz = pytz.timezone(timezone_name)
        local_time = utc_time.astimezone(tz)
        return local_time.strftime("%A, %B %d, %Y at %I:%M %p %Z")
    except Exception as e:
        print(f"Error formatting time: {e}")
        return "Invalid Time"

def initialize_services():
    """
    Initialize shared services like Gmail and OpenAI.
    Returns:
        dict: A dictionary of initialized services.
    """
    services = {}

    try:
        # Load OpenAI API Key
        services['openai_key'] = os.getenv("OPENAI_API_KEY")
        if not services['openai_key']:
            raise ValueError("OpenAI API key is missing in environment variables.")

        # Initialize Gmail API (OAuth2)
        creds = None
        # The token.json file stores the user's access and refresh tokens, and is created automatically when the
        # authorization flow completes for the first time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        # Build the Gmail service
        services['gmail'] = build('gmail', 'v1', credentials=creds)

        print("Services initialized successfully.")

    except Exception as e:
        print(f"Error initializing services: {e}")

    return services

