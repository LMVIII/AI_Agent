import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import openai
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# ==============================
# General Module
# ==============================
def general_module(content_frame, feedback_area, services):
    """Render the General Module."""
    clear_frame(content_frame)

    # Title
    tk.Label(content_frame, text="General Task Prompt", font=("Arial", 14, "bold")).pack(pady=10)

    # Input field for task
    tk.Label(content_frame, text="Enter your general task below:").pack()
    task_entry = tk.Entry(content_frame, width=70)
    task_entry.pack(pady=10)

    def run_task():
        prompt = task_entry.get().strip()
        if not prompt:
            log_to_feedback(feedback_area, "Error: Task prompt cannot be empty.")
            return
        execute_ai_task(prompt, feedback_area, "general", services)

    # Run Task Button
    tk.Button(
        content_frame,
        text="Run Task",
        command=run_task,
        bg="blue",
        fg="white",
        width=20
    ).pack(pady=10)


# ==============================
# Scheduling Module
# ==============================
def scheduling_module(content_frame, feedback_area, services):
    """Render the Scheduling Module."""
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

    # Schedule Task Button
    tk.Button(
        content_frame,
        text="Schedule Task",
        command=schedule_task,
        bg="green",
        fg="white",
        width=20
    ).pack(pady=10)


# ==============================
# Coding Module
# ==============================
def coding_module(content_frame, feedback_area, services):
    """Render the Coding Module."""
    clear_frame(content_frame)

    # Title
    tk.Label(content_frame, text="Coding Module", font=("Arial", 14, "bold")).pack(pady=10)

    # Input field
    coding_task_entry = create_labeled_entry(content_frame, "Enter your coding task below:")

    def generate_code():
        prompt = coding_task_entry.get().strip()
        if not prompt:
            log_to_feedback(feedback_area, "Error: Task prompt cannot be empty.")
            return
        execute_ai_task(prompt, feedback_area, "coding", services)

    # Generate Code Button
    tk.Button(
        content_frame,
        text="Generate Code",
        command=generate_code,
        bg="blue",
        fg="white",
        width=20
    ).pack(pady=10)


# ==============================
# Shared Utilities
# ==============================
def clear_frame(frame):
    """Clear all widgets from the frame."""
    for widget in frame.winfo_children():
        widget.destroy()


def log_to_feedback(feedback_area, message):
    """Log a message to the feedback area with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    feedback_area.insert(tk.END, f"[{timestamp}] {message}\n")
    feedback_area.see(tk.END)


def execute_ai_task(prompt, feedback_area, task_type, services):
    """Execute the AI task based on task type."""
    def ai_task():
        log_to_feedback(feedback_area, f"Processing {task_type} task: {prompt}")

        try:
            # Simulate API call
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            result = response['choices'][0]['message']['content']
            log_to_feedback(feedback_area, f"Result:\n{result}")
        except Exception as e:
            log_to_feedback(feedback_area, f"Error while processing task: {e}")

    threading.Thread(target=ai_task).start()


def create_labeled_entry(parent, label_text, width=50):
    """Create a labeled Entry widget."""
    tk.Label(parent, text=label_text).pack(pady=5)
    entry = tk.Entry(parent, width=width)
    entry.pack()
    return entry


# ==============================
# Main GUI
# ==============================
def launch_gui(services):
    """
    Launch the main GUI for the Mongoose AI Agent.
    Args:
        services (dict): A dictionary of initialized services (e.g., Gmail, OpenAI).
    """
    root = tk.Tk()
    root.title("Mongoose Submodularized GUI")
    root.geometry("900x700")

    # Sidebar for navigation
    sidebar = tk.Frame(root, width=200, bg="lightgray")
    sidebar.pack(side="left", fill="y")

    # Main content frame
    content_frame = tk.Frame(root, bg="white")
    content_frame.pack(side="right", fill="both", expand=True)

    # Feedback Area
    feedback_area = scrolledtext.ScrolledText(root, width=100, height=10)
    feedback_area.pack(side="bottom", fill="x")

    # Sidebar buttons
    tk.Button(
        sidebar,
        text="General",
        command=lambda: general_module(content_frame, feedback_area, services),
        width=20
    ).pack(pady=10)

    tk.Button(
        sidebar,
        text="Scheduling",
        command=lambda: scheduling_module(content_frame, feedback_area, services),
        width=20
    ).pack(pady=10)

    tk.Button(
        sidebar,
        text="Coding",
        command=lambda: coding_module(content_frame, feedback_area, services),
        width=20
    ).pack(pady=10)

    # Load default module
    general_module(content_frame, feedback_area, services)

    root.mainloop()
