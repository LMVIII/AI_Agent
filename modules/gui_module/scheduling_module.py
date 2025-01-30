import tkinter as tk
from tkinter import ttk
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import pickle

# If modifying the calendar, define the required SCOPES
SCOPES = ['https://www.googleapis.com/auth/calendar']

# List of staff email addresses
STAFF_EMAILS = [
    "andrew@profitandwealthtaxadvisors.com",
    "priscilla@profitandwealthtaxadvisors.com",
    "jessica@profitandwealthtaxadvisors.com"
]

ADMIN_EMAIL = "admin@profitandwealthtaxadvisors.com"

def authenticate_google_account(email=None):
    """Handles Google OAuth authentication."""
    creds = None
    # Token file stores the user's access and refresh tokens
    token_filename = f'token_{email}.pickle' if email else 'token.pickle'
    
    if os.path.exists(token_filename):
        with open(token_filename, 'rb') as token:
            creds = pickle.load(token)

    # If credentials are expired or missing, reauthenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for the next run
        with open(token_filename, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('calendar', 'v3', credentials=creds)

def get_free_busy_info(service, calendar_id, time_min, time_max):
    """Get free/busy information for the specified calendar."""
    freebusy_query = {
        "timeMin": time_min,
        "timeMax": time_max,
        "timeZone": 'America/Los_Angeles',
        "items": [{"id": calendar_id}]
    }
    
    events_result = service.freebusy().query(body=freebusy_query).execute()
    return events_result['calendars'][calendar_id].get('busy', [])

def create_event(service, summary, start_time, end_time, attendees):
    """Creates a calendar event and adds attendees."""
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/Los_Angeles',
        },
        'attendees': [{'email': email} for email in attendees],
    }

    event = service.events().insert(calendarId=ADMIN_EMAIL, body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")
    return event

def scheduling_module(content_frame, feedback_area, services):
    """
    Render the Scheduling Module and schedule the task.
    Args:
        content_frame: The frame where the module content is displayed.
        feedback_area: The text area where logs and messages are displayed.
        services: A dictionary containing initialized services (e.g., OpenAI, Gmail).
    """
    clear_frame(content_frame)

    # Title
    tk.Label(content_frame, text="Scheduling Module", font=("Arial", 14, "bold")).pack(pady=10)

    # Input fields
    client_name_entry = create_labeled_entry(content_frame, "Client Name:")
    client_email_entry = create_labeled_entry(content_frame, "Client Email Address:")

    tk.Label(content_frame, text="Reason:").pack(pady=5)
    reason_combo = ttk.Combobox(
        content_frame,
        values=["Tax Organizer Review", "Financial Statement Review", "Tax Planning & Projections", "Other"],
        width=40
    )
    reason_combo.pack()

    def schedule_task():
        client_name = client_name_entry.get().strip()
        client_email = client_email_entry.get().strip()
        reason = reason_combo.get().strip()

        # Basic validation
        if not client_name or not client_email or not reason:
            log_to_feedback(feedback_area, "Error: All fields are required.")
            return

        log_to_feedback(feedback_area, f"Scheduled task for {client_name} ({client_email}) - Reason: {reason}")

        # Authenticate and create event using Google Calendar API
        service = authenticate_google_account()

        # Example: Set event start and end times (hardcoded for now)
        start_time = "2025-01-01T10:00:00"
        end_time = "2025-01-01T11:00:00"

        # Gather all attendees: staff and client
        attendees = [client_email] + STAFF_EMAILS

        event = create_event(service, reason, start_time, end_time, attendees)

        # Output event link in feedback area (in GUI)
        log_to_feedback(feedback_area, f"Event created: {event.get('htmlLink')}")

    tk.Button(
        content_frame,
        text="Schedule Task",
        command=schedule_task,
        bg="green",
        fg="white",
        width=20
    ).pack(pady=10)

def clear_frame(frame):
    """Clear all widgets from the frame."""
    for widget in frame.winfo_children():
        widget.destroy()

def create_labeled_entry(parent, label_text, width=50):
    """Create a labeled Entry widget."""
    tk.Label(parent, text=label_text).pack(pady=5)
    entry = tk.Entry(parent, width=width)
    entry.pack()
    return entry

def log_to_feedback(feedback_area, message):
    """Log a message to the feedback area with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    feedback_area.insert(tk.END, f"[{timestamp}] {message}\n")
    feedback_area.see(tk.END)

