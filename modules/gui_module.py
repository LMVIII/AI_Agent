import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from modules.job_module import save_jobs_to_file, scheduling_jobs, update_gui
from modules.utils import STATE_TIMEZONE_MAPPING
from git import Repo
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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

def update_file_with_code(file_path, prompt, feedback_area):
    """Generate code and update the file."""
    feedback_area.insert(tk.END, f"Generating code for {file_path}...\n")
    feedback_area.see(tk.END)

    code = generate_code(prompt)
    if not code or code.startswith("Error"):
        feedback_area.insert(tk.END, f"Code generation failed: {code}\n")
        feedback_area.see(tk.END)
        return

    try:
        with open(file_path, "w") as file:
            file.write(code)
        feedback_area.insert(tk.END, f"Updated {file_path} successfully!\n")
        feedback_area.see(tk.END)
    except Exception as e:
        feedback_area.insert(tk.END, f"Error updating file {file_path}: {e}\n")
        feedback_area.see(tk.END)

def commit_and_push_changes(repo_path, commit_message, feedback_area):
    """Commit and push changes to GitHub."""
    try:
        repo = Repo(repo_path)
        repo.git.add(all=True)
        repo.index.commit(commit_message)
        origin = repo.remote(name='origin')
        origin.push()
        feedback_area.insert(tk.END, "Changes pushed to GitHub successfully!\n")
        feedback_area.see(tk.END)
    except Exception as e:
        feedback_area.insert(tk.END, f"Error committing and pushing changes: {e}\n")
        feedback_area.see(tk.END)

def launch_gui(gmail_service):
    root = tk.Tk()
    root.title("AI Agent - Scheduling Manager & AI Prompt Generator")
    root.geometry("800x600")

    # Existing scheduling inputs
    tk.Label(root, text="Client Name:").pack(pady=5)
    client_name_entry = tk.Entry(root, width=50)
    client_name_entry.pack()

    tk.Label(root, text="Client Email Address:").pack(pady=5)
    client_email_entry = tk.Entry(root, width=50)
    client_email_entry.pack()

    # New AI Prompt Section
    tk.Label(root, text="What do you want me to do?").pack(pady=5)
    ai_prompt_entry = tk.Entry(root, width=70)
    ai_prompt_entry.insert(0, "Add logging to the Google Calendar scheduling function.")
    ai_prompt_entry.pack(pady=5)

    tk.Label(root, text="File to Update (default: modules/calendar_module.py):").pack(pady=5)
    ai_file_entry = tk.Entry(root, width=50)
    ai_file_entry.insert(0, "modules/calendar_module.py")
    ai_file_entry.pack(pady=5)

    # Feedback Area
    feedback_area = scrolledtext.ScrolledText(root, width=90, height=15)
    feedback_area.pack(pady=10)

    def execute_ai_task():
        """Run the AI task in a separate thread."""
        def ai_task():
            file_path = ai_file_entry.get().strip()
            prompt = ai_prompt_entry.get().strip()

            if not file_path or not prompt:
                messagebox.showerror("Error", "Please provide both a file path and a prompt.")
                return

            feedback_area.insert(tk.END, f"Processing AI prompt: {prompt}\n")
            feedback_area.see(tk.END)

            update_file_with_code(file_path, prompt, feedback_area)

            commit_message = f"Updated {file_path} with changes: {prompt}"
            commit_and_push_changes("C:/Users/louie/MyPythonProjects/AI_Agent", commit_message, feedback_area)

        threading.Thread(target=ai_task).start()

    # Add button for AI Task
    tk.Button(root, text="Build with AI", command=execute_ai_task).pack(pady=10)

    # Existing scheduling functionality (trimmed for brevity)
    tk.Button(root, text="Schedule Meeting", command=lambda: print("Schedule logic here")).pack(pady=10)

    root.mainloop()
