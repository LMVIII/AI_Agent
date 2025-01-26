Here's a basic implementation using Google's Calendar API. This is a simplified example on how you can create the core functionalities of your module.

First, make sure to install the Google client library, you might also need the date-time library.

```sh
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
Here's a Python module to interact with Google's Calendar API:

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Load the credentials
credentials = service_account.Credentials.from_service_account_file(
    'path/to/your/service/account/key.json'
)

# Build the service
service = build('calendar', 'v3', credentials=credentials)

# Calendar ID, 'primary' means the current user's calendar
calendarId = 'primary'


def add_event(summary, location, description, start_time, end_time):
    start = start_time.isoformat()
    end = end_time.isoformat()

    event_result = service.events().insert(calendarId=calendarId,
                                           body={
                                               "summary": summary,
                                               "location": location,
                                               "description": description,
                                               "start": {"dateTime": start, "timeZone": 'America/Los_Angeles'},
                                               "end": {"dateTime": end, "timeZone": 'America/Los_Angeles'},
                                           }
                                           ).execute()

    print("created event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['dateTime'])
    print("ends at: ", event_result['end']['dateTime'])

    
# Usage example
if __name__ == '__main__':
    add_event(
        "Meeting with Bob",
        "123 Main St",
        "Discuss the Q4 sales forecast",
        datetime.now() + timedelta(days=1),
        datetime.now() + timedelta(days=1, hours=1)
    )
``` 

The `add_event()` function creates an event and prints some useful information about it.

Please replace `'path/to/your/service/account/key.json' with the actual path to your key file.

Also take note that you need to enable the Google Calendar API in the developer console to get your service account, which allows server-to-server interaction.

Additionally, this is only a basic start. You may need to handle exceptions and edge cases depending on your specific use-case. 

The Google Calendar API has many more features you can take advantage of, such as updating or deleting events, listing them, adding attendees, and much more. For more about Google Calendar API, you can check the official documentation: https://developers.google.com/calendar