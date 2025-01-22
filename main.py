from modules.utils import initialize_services
from modules.gui_module import launch_gui

def main():
    """
    Main entry point for the AI Agent.
    """
    print("Initializing AI Agent...")
    # Initialize Gmail and other services
    gmail_service = initialize_services()

    # Launch the GUI for scheduling management
    launch_gui(gmail_service)

if __name__ == "__main__":
    main()
