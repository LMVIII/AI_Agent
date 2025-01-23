import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def determine_task_type(prompt):
    """Use OpenAI to classify the task as 'scheduling' or 'general'."""
    classification_prompt = f"""
    Based on the following task, classify it as either 'scheduling' or 'general'.
    Task: {prompt}

    Guidelines:
    - If the task involves meetings, scheduling, or clients, classify as 'scheduling'.
    - Otherwise, classify as 'general'.

    Respond with 'scheduling' or 'general' only.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": classification_prompt}]
        )
        return response['choices'][0]['message']['content'].strip().lower()
    except Exception as e:
        return "general"

def generate_code(prompt):
    """Generate code using OpenAI API."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating code: {e}"

def update_file_with_code(prompt, feedback_area):
    """Generate code and update the file based on AI response."""
    feedback_area.insert(tk.END, "Connecting to OpenAI API...\n")
    feedback_area.see(tk.END)

    try:
        # Generate code and determine file from OpenAI
        response = generate_code(prompt)
        file_name, code = response.split("\n\n", 1)

        feedback_area.insert(tk.END, f"Updating file: {file_name.strip()}...\n")
        feedback_area.see(tk.END)

        # Write code to the file
        with open(file_name.strip(), "w") as file:
            file.write(code)
        feedback_area.insert(tk.END, "File updated successfully!\n")
        feedback_area.see(tk.END)
    except Exception as e:
        feedback_area.insert(tk.END, f"Error updating file: {e}\n")
        feedback_area.see(tk.END)

def execute_ai_task(prompt, feedback_area, scheduling_frame):
    """Run the AI task and dynamically adjust the GUI."""
    def ai_task():
        feedback_area.insert(tk.END, f"Processing AI prompt: {prompt}\n")
        feedback_area.see(tk.END)

        # Determine if task is related to scheduling
        task_type = determine_task_type(prompt)
        if task_type == "scheduling":
            feedback_area.insert(tk.END, "Task identified as scheduling.\n")
            scheduling_frame.pack(pady=10)
        else:
            feedback_area.insert(tk.END, "Task identified as general.\n")
            scheduling_frame.pack_forget()

        update_file_with_code(prompt, feedback_area)

    threading.Thread(target=ai_task).start()

def launch_gui():
    """Launch the main GUI for AI Agent."""
    root = tk.Tk()
    root.title("AI Agent - Scheduling Manager & AI Assistant")
    root.geometry("900x700")

    # Title for High-Level Prompt Section
    tk.Label(root, text="What do you want me to do?", font=("Arial", 14, "bold")).pack(pady=10)

    # AI Prompt Section
    ai_prompt_entry = tk.Entry(root, width=70)
    ai_prompt_entry.insert(0, "Add logging to the Google Calendar scheduling function.")
    ai_prompt_entry.pack(pady=10)

    # Feedback Area for Logs
    feedback_area = scrolledtext.ScrolledText(root, width=100, height=15)
    feedback_area.pack(pady=10)

    # Scheduling Section (hidden by default)
    scheduling_frame = tk.Frame(root)
    tk.Label(scheduling_frame, text="Client Name:").pack(pady=5)
    client_name_entry = tk.Entry(scheduling_frame, width=50)
    client_name_entry.pack()

    tk.Label(scheduling_frame, text="Client Email Address:").pack(pady=5)
    client_email_entry = tk.Entry(scheduling_frame, width=50)
    client_email_entry.pack()

    tk.Label(scheduling_frame, text="Reason:").pack(pady=5)
    reason_combo = ttk.Combobox(
        scheduling_frame,
        values=["Tax Organizer Review", "Financial Statement Review", "Tax Planning & Projections", "Other"],
        width=40,
    )
    reason_combo.pack()

    # Button to execute the AI task
    tk.Button(
        root,
        text="Run",
        command=lambda: execute_ai_task(ai_prompt_entry.get(), feedback_area, scheduling_frame),
        bg="green",
        fg="white",
        width=20
    ).pack(pady=10)

    root.mainloop()
