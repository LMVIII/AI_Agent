import os
import openai
from dotenv import load_dotenv
import subprocess
from git import Repo
from modules.gui_module import launch_gui  # Import the GUI function

# Load OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Generate code using OpenAI
def generate_code(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert software developer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

# Update project files
def update_file(file_path, prompt):
    print(f"Updating {file_path}...")
    code = generate_code(prompt)
    with open(file_path, "w") as f:
        f.write(code)
    print(f"{file_path} updated successfully!")

# Run tests
def run_tests():
    print("Running tests...")
    result = subprocess.run(["pytest"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode == 0:
        print("All tests passed!")
    else:
        print("Some tests failed. Check the output above.")

# Commit and push changes to GitHub
def commit_and_push(repo_path, commit_message):
    repo = Repo(repo_path)
    repo.git.add(all=True)
    repo.index.commit(commit_message)
    origin = repo.remote(name="origin")
    origin.push()
    print("Changes pushed to GitHub.")

# Main function to orchestrate tasks
def main():
    # Example: Update calendar_module.py
    update_file(
        "modules/calendar_module.py",
        "Create a Python module to schedule events in Google Calendar using OAuth2."
    )

    # Run tests
    run_tests()

    # Commit and push changes
    commit_and_push(
        repo_path="C:/Users/louie/MyPythonProjects/AI_Agent",
        commit_message="AI-generated update for calendar_module.py"
    )

    # Launch the GUI
    print("Launching the GUI...")
    launch_gui()  # Call the GUI from gui_module.py

if __name__ == "__main__":
    main()
