import tkinter as tk
from tkinter import scrolledtext
from modules.gui_module.general_module import general_module
from modules.gui_module.scheduling_module import scheduling_module
from modules.gui_module.coding_module import coding_module

def launch_gui(services):
    """
    Launch the main GUI for the Mongoose AI Agent.
    Args:
        services (dict): A dictionary of initialized services (e.g., Gmail, OpenAI).
    """
    root = tk.Tk()
    root.title("Mongoose Submodularized GUI")
    root.geometry("900x700")

    # Sidebar for navigation
    sidebar = tk.Frame(root, width=200, bg="lightgray")
    sidebar.pack(side="left", fill="y")

    # Main content frame
    content_frame = tk.Frame(root, bg="white")
    content_frame.pack(side="right", fill="both", expand=True)

    # Feedback Area
    feedback_area = scrolledtext.ScrolledText(root, width=100, height=10)
    feedback_area.pack(side="bottom", fill="x")

    # Sidebar buttons
    tk.Button(
        sidebar,
        text="General",
        command=lambda: general_module(content_frame, feedback_area, services),
        width=20
    ).pack(pady=10)

    tk.Button(
        sidebar,
        text="Scheduling",
        command=lambda: scheduling_module(content_frame, feedback_area, services),
        width=20
    ).pack(pady=10)

    tk.Button(
        sidebar,
        text="Coding",
        command=lambda: coding_module(content_frame, feedback_area, services),
        width=20
    ).pack(pady=10)

    # Load default module
    general_module(content_frame, feedback_area, services)

    # Start Tkinter's main loop to display the GUI
    root.mainloop()
