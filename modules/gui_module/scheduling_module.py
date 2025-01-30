import tkinter as tk
from tkinter import ttk
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import pickle

# Google Calendar API Scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Updated Staff emails with Louie and Erin
STAFF_EMAILS = [
    "andrew@profitandwealthtaxadvisors.com",
    "priscilla@profitandwealthtaxadvisors.com",
    "jessica@profitandwealthtaxadvisors.com",
    "louie@profitandwealthtaxadvisors.com",
    "erin@profitandwealthtaxadvisors.com"
]

ADMIN_EMAIL = "admin@profitandwealthtaxadvisors.com"

# Function to authenticate Google Calendar API
def authenticate_google_account():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('calendar', 'v3', credentials=creds)

# Function to create a Google Calendar event
def create_event(service, summary, start_time, end_time, attendees):
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
    tk.Label(content_frame, text="Time Zone:").grid(row=4, column=0, pady=5, sticky="w")
    timezone_combo = ttk.Combobox(
        content_frame,
        values=["PST", "EST", "CST", "MST"],
        width=40
    )
    timezone_combo.grid(row=4, column=1, pady=5)

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
    
    def schedule_task():
        client_name = client_name_entry.get().strip()
        client_email = client_email_entry.get().strip()
        reason = reason_combo.get().strip()
        timezone = timezone_combo.get().strip()
        priority = priority_combo.get().strip()
        secondary_person = secondary_person_combo.get().strip()
        third_person = third_person_combo.get().strip()

        # Validation
        if not client_name or not client_email or not reason or not timezone or not priority:
            log_to_feedback(feedback_area, "Error: All fields are required.")
            return

        # Schedule event using Google Calendar API
        service = authenticate_google_account()

        # Define start and end times (you can make this dynamic based on user input)
        start_time = "2025-01-01T10:00:00"
        end_time = "2025-01-01T11:00:00"

        # Attendees: client + secondary + third person
        attendees = [client_email, secondary_person, third_person]

        # Create event
        event = create_event(service, reason, start_time, end_time, attendees)

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

