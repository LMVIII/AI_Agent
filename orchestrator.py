import openai
import subprocess
from git import Repo
from modules.gui_module.launch_gui import launch_gui  # Import the GUI function
from services import get_services  # Import get_services from services.py

# Get OpenAI API key from services dictionary passed from main.py
def get_openai_api_key(services):
    openai_api_key = services.get("openai_key")
    if not openai_api_key:
        raise ValueError("OpenAI API key is missing in environment variables.")
    return openai_api_key

# Set OpenAI API key for this script
def set_openai_key(services):
    openai.api_key = get_openai_api_key(services)  # Use services to get API key

# Generate code using OpenAI
def generate_code(prompt, services):
    set_openai_key(services)  # Set the OpenAI key dynamically

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[  # Adding system instruction for the model
            {"role": "system", "content": "You are an expert software developer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

# Update project files (e.g., calendar_module.py)
def update_file(file_path, prompt, services):
    print(f"Updating {file_path}...")
    code = generate_code(prompt, services)
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
def main(services):
    # Example: Update calendar_module.py with AI-generated code
    update_file(
        "modules/calendar_module.py",
        "Create a Python module to schedule events in Google Calendar using OAuth2.",
        services
    )

    # Run tests after updating files
    run_tests()

    # Commit and push changes to GitHub
    commit_and_push(
        repo_path="C:/Users/louie/MyPythonProjects/AI_Agent",
        commit_message="AI-generated update for calendar_module.py"
    )

    # Launch the GUI
    print("Launching the GUI...")
    launch_gui(services)  # Pass services to the GUI

if __name__ == "__main__":
    # Ensure services are passed to orchestrator
    services = get_services()  # Get services from services.py
    main(services)
