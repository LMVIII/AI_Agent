import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
import pytz
import tkinter as tk
from tkinter import ttk

# Google Calendar API Scopes
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/gmail.send']

# List of staff emails
STAFF_EMAILS = [
    "andrew@profitandwealthtaxadvisors.com",
    "priscilla@profitandwealthtaxadvisors.com",
    "jessica@profitandwealthtaxadvisors.com",
    "louie@profitandwealthtaxadvisors.com",
    "erin@profitandwealthtaxadvisors.com"
]

ADMIN_EMAIL = "admin@profitandwealthtaxadvisors.com"

# Function to authenticate Google Calendar API
def authenticate_google_account(email=None):
    """Handles Google OAuth authentication for a specific email."""
    creds = None
    # Use a separate token file for each email (e.g., token_andrew.pickle, token_priscilla.pickle, etc.)
    token_filename = f'token_{email}.pickle' if email else 'token.pickle'
    
    # Check if the token file already exists
    if os.path.exists(token_filename):
        with open(token_filename, 'rb') as token:
            creds = pickle.load(token)
    
    # If no credentials or the credentials are invalid, request new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(token_filename, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('calendar', 'v3', credentials=creds), build('gmail', 'v1', credentials=creds)

# Function to authenticate the admin email and staff emails
def authenticate_all_accounts():
    """Authenticate the admin account and all staff accounts."""
    # Authenticate the admin account
    admin_service, admin_gmail_service = authenticate_google_account(ADMIN_EMAIL)

    # Authenticate all staff accounts and store services in a dictionary
    staff_services = {}
    for email in STAFF_EMAILS:
        staff_services[email] = authenticate_google_account(email)[0]  # Only calendar service is needed for staff

    return admin_service, admin_gmail_service, staff_services

# Function to create an event on the admin calendar
def create_event(service, summary, start_time, end_time, attendees):
    """Create a Google Calendar event."""
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/Los_Angeles',  # Admin calendar time zone
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

# Function to send confirmation and rescheduling emails (client only)
def send_email(service, to, subject, body):
    """Send an email using the Gmail API."""
    message = {
        'to': to,
        'subject': subject,
        'body': body,
    }
    create_message(service, to, subject, body)

def create_message(service, to, subject, body):
    """Create the email message and send it using the Gmail API."""
    message = service.users().messages().send(
        userId="me", body={
            'raw': create_raw_message(to, subject, body)
        }
    ).execute()
    print(f"Message sent to {to}: {subject}")

def create_raw_message(to, subject, body):
    """Create a raw email message."""
    message = f"To: {to}\r\nSubject: {subject}\r\n\r\n{body}\r\n\nBest regards,\nYour Team at Profit and Wealth Tax Advisors"
    return message.encode('utf-8').decode('ascii')

# Function to handle scheduling task
def scheduling_module(content_frame, feedback_area, services):
    clear_frame(content_frame)

    # Title
    tk.Label(content_frame, text="Scheduling Module", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    # Input fields (using grid for better control)
    client_name_entry = create_labeled_entry(content_frame, "Client Name:", 1, 0)
    client_email_entry = create_labeled_entry(content_frame, "Client Email Address:", 2, 0)

    tk.Label(content_frame, text="Reason:").grid(row=3, column=0, pady=5, sticky="w")
    reason_combo = ttk.Combobox(
        content_frame,
        values=["Tax Organizer Review", "Financial Statement Review", "Tax Planning & Projections", "Other"],
        width=40
    )
    reason_combo.grid(row=3, column=1, pady=5)

    # Time zone field
    tk.Label(content_frame, text="Client Time Zone:").grid(row=4, column=0, pady=5, sticky="w")
    client_timezone_combo = ttk.Combobox(
        content_frame,
        values=["PST", "EST", "CST", "MST"],
        width=40
    )
    client_timezone_combo.grid(row=4, column=1, pady=5)

    # Priority level field
    tk.Label(content_frame, text="Priority Level:").grid(row=5, column=0, pady=5, sticky="w")
    priority_combo = ttk.Combobox(
        content_frame,
        values=["1", "2", "3"],
        width=40
    )
    priority_combo.grid(row=5, column=1, pady=5)

    # Secondary and third person selection
    tk.Label(content_frame, text="Secondary Person:").grid(row=6, column=0, pady=5, sticky="w")
    secondary_person_combo = ttk.Combobox(
        content_frame,
        values=STAFF_EMAILS,
        width=40
    )
    secondary_person_combo.grid(row=6, column=1, pady=5)

    tk.Label(content_frame, text="Third Person (Optional):").grid(row=7, column=0, pady=5, sticky="w")
    third_person_combo = ttk.Combobox(
        content_frame,
        values=STAFF_EMAILS,
        width=40
    )
    third_person_combo.grid(row=7, column=1, pady=5)

    # Tracker for scheduling progress
    tracker_label = tk.Label(content_frame, text="Scheduling Progress:", font=("Arial", 12))
    tracker_label.grid(row=8, column=0, pady=10, sticky="w")
    
    tracker_area = tk.Text(content_frame, height=4, width=40)  # Wider rectangle
    tracker_area.grid(row=9, column=0, columnspan=2, pady=10)

    # Authenticate and create event
    def schedule_task():
        client_name = client_name_entry.get().strip()
        client_email = client_email_entry.get().strip()
        reason = reason_combo.get().strip()
        timezone = client_timezone_combo.get().strip()
        priority = priority_combo.get().strip()
        secondary_person = secondary_person_combo.get().strip()
        third_person = third_person_combo.get().strip()

        # Validation
        if not client_name or not client_email or not reason or not timezone or not priority:
            log_to_feedback(feedback_area, "Error: All fields are required.")
            return

        # Authenticate and create event using Google Calendar API
        admin_service, admin_gmail_service, staff_services = authenticate_all_accounts()

        # Define start and end times (you can make this dynamic based on user input)
        start_time = "2025-01-01T10:00:00"
        end_time = "2025-01-01T11:00:00"

        # Adjust start and end times based on the client's time zone
        client_tz = pytz.timezone(timezone)
        pst_tz = pytz.timezone('America/Los_Angeles')

        start_time_pst = datetime(2025, 1, 1, 10, 0, 0, tzinfo=pst_tz)
        start_time_client = start_time_pst.astimezone(client_tz)

        end_time_pst = datetime(2025, 1, 1, 11, 0, 0, tzinfo=pst_tz)
        end_time_client = end_time_pst.astimezone(client_tz)

        # Convert datetime to string for event creation
        start_time = start_time_client.strftime('%Y-%m-%dT%H:%M:%S')
        end_time = end_time_client.strftime('%Y-%m-%dT%H:%M:%S')

        # Attendees: client + secondary + third person
        attendees = [client_email, secondary_person, third_person]

        # Create event using the admin service
        event = create_event(admin_service, reason, start_time, end_time, attendees)

        # Send confirmation email to client only
        send_email(admin_gmail_service, client_email, "Confirmation: Your Meeting Scheduled", "Your meeting has been confirmed.")
        
        log_to_feedback(feedback_area, f"Event created: {event.get('htmlLink')}")

    # Schedule Task Button
    tk.Button(
        content_frame,
        text="Schedule Task",
        command=schedule_task,
        bg="green",
        fg="white",
        width=20
    ).grid(row=10, column=0, columnspan=2, pady=10)

# Utility functions (clear_frame, create_labeled_entry, log_to_feedback)
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create_labeled_entry(parent, label_text, row, col, width=50):
    tk.Label(parent, text=label_text).grid(row=row, column=col, pady=5, sticky="w")
    entry = tk.Entry(parent, width=width)
    entry.grid(row=row, column=col + 1, pady=5)
    return entry

def log_to_feedback(feedback_area, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    feedback_area.insert(tk.END, f"[{timestamp}] {message}\n")
    feedback_area.see(tk.END)

