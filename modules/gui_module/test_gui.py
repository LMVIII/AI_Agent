import sys
import os

# Add the root directory to the Python path to make 'modules' recognizable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Now you can import 'modules' from anywhere in the project
from modules.gui_module.launch_gui import launch_gui

# Mock services for testing
services = {"openai_key": "dummy_key"}  # Replace with actual mock data as needed

# Launch the GUI with the mocked services
launch_gui(services)
