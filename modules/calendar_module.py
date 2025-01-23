In order to schedule events in Google Calendar using OAuth2, we'll need to first install the `google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`, and `google-api-python-client` libraries. We also need a credentials.json file which is obtained from Google Cloud Console for the OAuth2 part.

Here is a Python module named schedule_event.py:

```python
import datetime
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Define the SCOPES. If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def schedule_event(summary, location, description, start_time, end_time):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    service = build('calendar', 'v3', credentials=creds)

    event = {
      'summary': summary,
      'location': location,
      'description': description,
      'start': {
        'dateTime': start_time,
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': end_time,
        'timeZone': 'America/Los_Angeles',
      },
    }

    # Call the Calendar API
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
```

You can use the function in the Python module with the necessary parameters. The start and end times should be in this format: 'yyyy-mm-ddThh:mm:ss'. 

Ensure you replace 'credentials.json' with your own OAuth2.0 Client ID.json downloaded when you created credentials at Google Cloud Console. Make sure to enable Calendar API for your project at the Google Cloud Console. Make sure you share the calendar with the client_id found in the credentials file and give it manage events permissions.

Disclaimer: The code above assumes the user running this script has proper environment and OS level permissions to read/write files and execute this script as well as access to the internet to make requests to the Google Calendar API. Error handling for exceptions and edge-cases has been kept minimal to maintain clarity and readability of code. In a production level code, appropriate error handling and logging must be implemented. Furthermore, appropriate security measures must be taken while storing credentials.json and token.pickle file.