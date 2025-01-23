from modules.gui_module.launch_gui import launch_gui
from modules.utils import initialize_services


def main():
    """
    Main entry point for the Mongoose AI Agent.
    """
    print("Initializing AI Agent...")

    # Initialize shared services
    services = initialize_services()

    # Launch the GUI with services
    launch_gui(services)


if __name__ == "__main__":
    main()
