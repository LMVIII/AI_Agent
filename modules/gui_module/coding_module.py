import tkinter as tk
from datetime import datetime


def coding_module(content_frame, feedback_area, services):
    """
    Render the Coding Module.
    Args:
        content_frame: The frame where the module content is displayed.
        feedback_area: The text area where logs and messages are displayed.
        services: A dictionary containing initialized services (e.g., OpenAI, Gmail).
    """
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

        # Example: Using OpenAI API from services
        openai_key = services.get("openai_key")
        if not openai_key:
            log_to_feedback(feedback_area, "Error: OpenAI API key is missing.")
            return

        log_to_feedback(feedback_area, f"Processing coding task: {prompt}")

    # Generate Code Button
    tk.Button(
        content_frame,
        text="Generate Code",
        command=generate_code,
        bg="blue",
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

