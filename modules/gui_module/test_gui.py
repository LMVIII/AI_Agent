from modules.gui_module.launch_gui import launch_gui

# Mocked services for testing
services = {
    "openai_key": "dummy_key"  # Mock the OpenAI API key
}

# Run the GUI independently
launch_gui(services)
