import openai
import subprocess
from git import Repo

def get_openai_api_key(services):
    openai_api_key = services.get("openai_key")
    if not openai_api_key:
        raise ValueError("OpenAI API key is missing in environment variables.")
    return openai_api_key

def set_openai_key(services):
    openai.api_key = get_openai_api_key(services)  # Use services to get API key

def generate_code(prompt, services):
    set_openai_key(services)  # Set the OpenAI key dynamically

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert software developer."},
                  {"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def update_file(file_path, prompt, services):
    print(f"Updating {file_path}...")
    code = generate_code(prompt, services)
    with open(file_path, "w") as f:
        f.write(code)
    print(f"{file_path} updated successfully!")

def run_tests():
    print("Running tests...")
    try:
        result = subprocess.run(["pytest"], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode == 0:
            print("All tests passed!")
        else:
            print("Some tests failed. Check the output above.")
    except subprocess.CalledProcessError as e:
        print(f"Error during test execution: {e}")

def commit_and_push(repo_path, commit_message):
    repo = Repo(repo_path)
    repo.git.add(all=True)
    repo.index.commit(commit_message)
    origin = repo.remote(name="origin")
    origin.push()
    print("Changes pushed to GitHub.")

def main(services):
    # Example: Update calendar_module.py with AI-generated code
    update_file("modules/calendar_module.py", 
                "Create a Python module to schedule events in Google Calendar using OAuth2.", 
                services)

    # Run tests after updating files
    run_tests()

    # Commit and push changes to GitHub
    commit_and_push(repo_path="C:/Users/louie/MyPythonProjects/AI_Agent", 
                    commit_message="AI-generated update for calendar_module.py")

if __name__ == "__main__":
    from services import get_services
    services = get_services()  # Get services from services.py
    main(services)
