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
        launch_gui(services)  # Launch the GUI
    except KeyboardInterrupt:
        # Gracefully exit if the user interrupts the process (e.g., closes GUI)
        print("GUI closed, exiting...")
    except Exception as e:
        print(f"Unexpected error during GUI launch: {e}")
    finally:
        # Ensure the program exits once the GUI is closed
        print("GUI has been closed.")
        exit()  # Exit immediately after closing the GUI to prevent reopening

if __name__ == "__main__":
    main()

