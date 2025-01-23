import tkinter as tk
from tkinter import ttk
from datetime import datetime


def scheduling_module(content_frame, feedback_area, services):
    """
    Render the Scheduling Module.
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

        # Example: Using Gmail service from services
        if "gmail" in services:
            log_to_feedback(feedback_area, "Gmail service is ready for task follow-up!")

    # Schedule Task Button
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


