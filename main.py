from dotenv import load_dotenv
from modules.utils import initialize_services
from modules.gui_module.launch_gui import launch_gui

# Load environment variables from .env file (this is done once in main.py)
load_dotenv()

def main():
    """
    Main entry point for the Mongoose AI Agent.
    """
    print("Initializing AI Agent...")

    # Initialize shared services (including the OpenAI API key)
    services = initialize_services()

    # Debugging: Ensure services contain the OpenAI API key
    print(f"OpenAI API Key from services: {services.get('openai_key')}")

    # Pass the services to orchestrator (import orchestrator and pass services)
    from orchestrator import main as orchestrator_main
    orchestrator_main(services)  # Pass services to orchestrator main function

    # Launch the GUI with services
    launch_gui(services)

if __name__ == "__main__":
    main()
