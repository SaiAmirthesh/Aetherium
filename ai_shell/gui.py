import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from .nlp import nlp_to_command
from .executor import execute_command

def run_app():
    # Main window
    root = tk.Tk()
    root.title("Aetherium AI Shell")
    root.geometry("650x400")

    # Input label and field
    input_label = tk.Label(root, text="Enter your request:")
    input_label.pack(pady=(10, 0))
    user_input = tk.Entry(root, width=80)
    user_input.pack(pady=5)

    # Output area
    output_area = ScrolledText(root, height=15, width=80, state="normal")
    output_area.pack(pady=10)

    def on_run():
        prompt = user_input.get()
        if not prompt.strip():
            output_area.insert(tk.END, "Please enter a request.\n")
            return

        output_area.insert(tk.END, f"User: {prompt}\n")
        output_area.insert(tk.END, "Processing...\n")
        root.update()

        command = nlp_to_command(prompt)
        output_area.insert(tk.END, f"Shell Command: {command}\n")
        output = execute_command(command)
        output_area.insert(tk.END, f"Output:\n{output}\n\n")
        output_area.see(tk.END)

    run_button = tk.Button(root, text="Run", command=on_run)
    run_button.pack(pady=5)

    root.mainloop()