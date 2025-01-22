import tkinter as tk
from tkinter import ttk, messagebox
import threading
from modules.job_module import save_jobs_to_file, scheduling_jobs, update_gui
from modules.utils import STATE_TIMEZONE_MAPPING

def launch_gui(gmail_service):
    root = tk.Tk()
    root.title("AI Agent - Scheduling Manager")

    tk.Label(root, text="Client Name:").pack(pady=5)
    client_name_entry = tk.Entry(root, width=50)
    client_name_entry.pack()

    tk.Label(root, text="Client Email Address:").pack(pady=5)
    client_email_entry = tk.Entry(root, width=50)
    client_email_entry.pack()

    tk.Label(root, text="Year:").pack(pady=5)
    year_combo = ttk.Combobox(root, values=[str(y) for y in range(2019, 2026)], width=10)
    year_combo.pack()

    tk.Label(root, text="Period:").pack(pady=5)
    period_category_combo = ttk.Combobox(root, values=["Month", "Quarter", "Annual"], width=20)
    period_category_combo.pack()

    specific_period_label = tk.Label(root, text="Specific Period:")
    specific_period_label.pack(pady=5)
    specific_period_combo = ttk.Combobox(root, values=[], width=20)
    specific_period_combo.pack()

    def on_period_category_change(event):
        category = period_category_combo.get()
        if category == "Month":
            specific_period_label.config(text="Specific Month:")
            specific_period_combo['values'] = [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ]
            specific_period_combo.set("")  # Clear selection
            specific_period_combo.configure(state="normal")
        elif category == "Quarter":
            specific_period_label.config(text="Specific Quarter:")
            specific_period_combo['values'] = ["Q1", "Q2", "Q3", "Q4"]
            specific_period_combo.set("")  # Clear selection
            specific_period_combo.configure(state="normal")
        elif category == "Annual":
            specific_period_label.config(text="")
            specific_period_combo.set("Annual")
            specific_period_combo.configure(state="disabled")

    period_category_combo.bind("<<ComboboxSelected>>", on_period_category_change)

    tk.Label(root, text="Reason:").pack(pady=5)
    reason_combo = ttk.Combobox(
        root,
        values=["Tax Organizer Review", "Financial Statement Review", "Tax Planning & Projections", "Tax Filings", "Other"],
        width=30,
    )
    reason_combo.pack()

    custom_reason_frame = tk.Frame(root)
    custom_reason_label = tk.Label(custom_reason_frame, text="Custom Reason (if 'Other'):")
    custom_reason_entry = tk.Entry(custom_reason_frame, width=50)

    def on_reason_change(event):
        if reason_combo.get() == "Other":
            custom_reason_frame.pack(pady=5, after=reason_combo)
            custom_reason_label.pack(side="left", padx=5)
            custom_reason_entry.pack(side="right", padx=5)
        else:
            custom_reason_frame.pack_forget()

    reason_combo.bind("<<ComboboxSelected>>", on_reason_change)

    tk.Label(root, text="Priority (1 = High, 2 = Medium, 3 = Low):").pack(pady=5)
    priority_combo = ttk.Combobox(root, values=["1", "2", "3"], width=5)
    priority_combo.pack()

    tk.Label(root, text="Client State:").pack(pady=5)
    state_combo = ttk.Combobox(root, values=list(STATE_TIMEZONE_MAPPING.keys()), width=30)
    state_combo.pack()

    selected_timezone = tk.StringVar(value="America/New_York")

    def on_state_selection():
        selected_state = state_combo.get()
        if selected_state:
            timezone_name = STATE_TIMEZONE_MAPPING.get(selected_state, "America/New_York")
            selected_timezone.set(timezone_name)
            messagebox.showinfo("Time Zone Updated", f"Time zone set to {timezone_name} for {selected_state}")
        else:
            messagebox.showerror("Error", "Please select a valid state.")

    state_combo.bind("<<ComboboxSelected>>", lambda event: on_state_selection())

    tk.Label(root, text="Ongoing Scheduling Jobs:").pack(pady=10)
    columns = ("ID", "Client Name", "Subject", "Priority", "Progress")
    job_list = ttk.Treeview(root, columns=columns, show="headings", height=10)
    for col in columns:
        job_list.heading(col, text=col)
    job_list.pack(pady=5)

    def execute_command():
        def schedule_task():
            client_name = client_name_entry.get().strip()
            client_email = client_email_entry.get().strip()
            year = year_combo.get().strip()
            period = specific_period_combo.get().strip()
            reason = reason_combo.get().strip()
            if reason == "Other":
                reason = custom_reason_entry.get().strip()
            priority = priority_combo.get().strip()

            if not all([client_name, client_email, year, period, reason, priority]):
                messagebox.showerror("Error", "All fields must be filled out.")
                return

            # Example scheduling logic
            print(f"Scheduling meeting for {client_name} ({client_email})")
            # Update GUI after task completes
            update_gui(job_list)

        threading.Thread(target=schedule_task).start()

    tk.Button(root, text="Schedule Meeting", command=execute_command).pack(pady=10)

    tk.Button(root, text="Delete Selected Job", command=lambda: delete_selected_job(job_list)).pack(pady=5)

    update_gui(job_list)
    root.mainloop()


