import json
from datetime import datetime

JOBS_FILE = "scheduling_jobs.json"
scheduling_jobs = {}

def save_jobs_to_file():
    """
    Save the scheduling jobs to a JSON file.
    """
    try:
        with open(JOBS_FILE, "w") as file:
            json.dump(scheduling_jobs, file, default=str)
        print("Jobs saved to file.")
    except Exception as e:
        print(f"Error saving jobs: {e}")

def load_jobs_from_file():
    """
    Load scheduling jobs from a JSON file.
    """
    global scheduling_jobs
    if os.path.exists(JOBS_FILE):
        try:
            with open(JOBS_FILE, "r") as file:
                jobs = json.load(file)
                for job_id, job in jobs.items():
                    job["last_action"] = datetime.fromisoformat(job["last_action"])
                scheduling_jobs = {int(job_id): job for job_id, job in jobs.items()}
            print("Jobs loaded from file.")
        except Exception as e:
            print(f"Error loading jobs: {e}")

def update_gui(job_list):
    """
    Update the GUI with job information and handle automatic deletion at 100% progress.
    """
    job_list.delete(*job_list.get_children())
    for job_id, job in list(scheduling_jobs.items()):  # Use list to allow modifications during iteration
        if job["progress"] == 100:
            del scheduling_jobs[job_id]  # Automatically delete completed jobs
        else:
            job_list.insert(
                "", "end",
                values=(
                    job_id,
                    job["client_name"],
                    job["subject"],
                    job["priority"],
                    f"{job['progress']}%"
                )
            )
    save_jobs_to_file()
