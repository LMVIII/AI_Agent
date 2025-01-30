from services import get_services  # Import get_services from services.py
from modules.gui_module.launch_gui import launch_gui
from orchestrator import main as orchestrator_main

def main():
    """
    Main entry point for the Mongoose AI Agent.
    """
    print("Initializing AI Agent...")

    # Get services (including the OpenAI API key and other services)
    services = get_services()

    # Debugging: Ensure services contain the OpenAI API key
    print(f"OpenAI API Key from services: {services.get('openai_key')}")

    # Pass the services to orchestrator
    orchestrator_main(services)

    # Launch the GUI with services after orchestration is complete
    try:
        launch_gui(services)
    except Exception as e:
        print(f"Error launching the GUI: {e}")

if __name__ == "__main__":
    main()
