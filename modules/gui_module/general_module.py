import tkinter as tk
from datetime import datetime


def general_module(content_frame, feedback_area, services):
    """
    Render the General Module.
    Args:
        content_frame: The frame where the module content is displayed.
        feedback_area: The text area where logs and messages are displayed.
        services: A dictionary containing initialized services (e.g., OpenAI, Gmail).
    """
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

        # Example: Using OpenAI API from services
        openai_key = services.get("openai_key")
        if not openai_key:
            log_to_feedback(feedback_area, "Error: OpenAI API key is missing.")
            return

        # Log the start of the task
        log_to_feedback(feedback_area, f"Processing general task: {prompt}")

        # Simulate OpenAI API call (replace with actual API logic)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            result = response['choices'][0]['message']['content']
            log_to_feedback(feedback_area, f"Result:\n{result}")
        except Exception as e:
            log_to_feedback(feedback_area, f"Error while processing task: {e}")

    # Run Task Button
    tk.Button(
        content_frame,
        text="Run Task",
        command=run_task,
        bg="blue",
        fg="white",
        width=20
    ).pack(pady=10)


def clear_frame(frame):
    """Clear all widgets from the frame."""
    for widget in frame.winfo_children():
        widget.destroy()


def log_to_feedback(feedback_area, message):
    """Log a message to the feedback area with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    feedback_area.insert(tk.END, f"[{timestamp}] {message}\n")
    feedback_area.see(tk.END)


