Creating a Python module that interacts with the Google Calendar API to schedule events involves several steps. Here's a guide, but note that this gets in-depth and advanced very quickly. 

This program assumes you have Python properly installed on your device, and then you should install the required Python libraries using pip.

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Following is a skeleton of a Python module named `gcal_scheduler.py` using OAuth2:

```python
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def google_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)


def create_event(service, calendar_id: str, start_time_str: str, end_time_str: str, 
                 summary: str, description: str, location: str):
    start = datetime.datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S")
    end = datetime.datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M:%S")

    event_result = service.events().insert(calendarId=calendar_id, 
                                           body={
                                               "summary": summary,
                                               "description": description,
                                               "start": {"dateTime": start.isoformat()},
                                               "end": {"dateTime": end.isoformat()},
                                               "location": location,
                                           }
                                           ).execute()

    return event_result['id']


if __name__ == "__main__":
    # Call this function to get the google calendar service object 
    service = google_calendar_service() 

    # event details
    start = "2019-07-25T00:00:00"
    end = "2019-07-26T00:00:00"
    summary = "Meeting with Bob"
    description = "Discuss the new project"
    location = "Conference Room A"

    calendar_id = 'primary' # add your calendar id here

    create_event(service, calendar_id, start, end, summary, description, location)
```

This code first tries to authenticate using the saved `token.json` file. If it's not present or is invalid, it falls back to using `credentials.json` and saves a new `token.json` file.

`create_event` function accepts event details and makes a request to Google Calendar API to create an event.

The `credentials.json` file contains your OAuth2 client ID and secret. You can get it from https://console.cloud.google.com/apis/credentials after creating a project and enabling the Google Calendar API.

The code above uses the 'primary' calendar. If you want to use a different calendar, replace 'primary' with your calendar ID.

This is a very basic script, and for production use you should add more error checking/handling, etc.