In order to interact with Google Calendar using Python, we'll use Google Calendar API. Here is a simple Python module that authenticates using OAuth2 and schedules an event.

Install these dependencies if not installed already:
```shell
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

Here is the Python code:

```python
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar']

def service_account_login():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

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

def create_event(service, start_time_str, end_time_str, summary, description, location):
    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

    event_result = service.events().insert(calendarId='primary',
        body={
            "summary": summary,
            "description": description,
            "location": location,
            "start": {
                "dateTime": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": 'America/Los_Angeles',
            },
            "end": {
                "dateTime": end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": 'America/Los_Angeles',
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 24 * 60},
                    {"method": "popup", "minutes": 10},
                ],
            },
        }
    ).execute()

    print(f"Created event {event_result['summary']}")

if __name__ == "__main__":
    service = service_account_login()
    start_time_str = "2022-01-01 09:00:00"
    end_time_str = "2022-01-01 10:00:00"
    summary = "Sample Event"
    description = "This is a sample description"
    location = "Los Angeles, CA"
    create_event(service, start_time_str, end_time_str, summary, description, location)
```
Please replace 'credentials.json' with your own OAuth 2.0 Client ID JSON file which you can download from Google Cloud Platform Console and adjust the time and details of the event in the `if __name__ == "__main__"` block to fit your needs. 

Keep in mind that Google’s OAuth 2.0 process requires consent screen configuration for your application where you define your application’s name, support contact, the scope of access, a domain name, and a redirect URI.
