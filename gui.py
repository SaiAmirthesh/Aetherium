import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from brain import AetheriumBrain
from commands import (
    handle_system_command,
    list_files,
    create_file,
    read_file,
    delete_file,
    execute_command
)
from config import GUI_CONFIG, APP_CONFIG

class AetheriumGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(GUI_CONFIG["window_title"])
        self.root.geometry(GUI_CONFIG["window_size"])
        
        self.brain = AetheriumBrain()
        self.setup_gui()
    
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text=f"🤖 {APP_CONFIG['name']} v{APP_CONFIG['version']}",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(input_frame, text="Enter your command:").grid(row=0, column=0, sticky=tk.W)
        
        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(
            input_frame, 
            textvariable=self.input_var, 
            width=50,
            font=(GUI_CONFIG["font_family"], GUI_CONFIG["font_size"])
        )
        self.input_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.input_entry.bind('<Return>', lambda e: self.process_input())
        
        # Buttons
        self.process_btn = ttk.Button(input_frame, text="Process", command=self.process_input)
        self.process_btn.grid(row=1, column=1, padx=(5, 0))
        
        # Output area
        ttk.Label(main_frame, text="Output:").grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        
        self.output_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=(GUI_CONFIG["font_family"], GUI_CONFIG["font_size"])
        )
        self.output_text.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))
        
        # Quick buttons frame
        quick_frame = ttk.Frame(main_frame)
        quick_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        quick_commands = [
            ("List Files", "list files"),
            ("System Info", "system info"),
            ("Processes", "running processes"),
            ("Disk Usage", "disk usage"),
            ("Create File", "create test.txt"),
            ("Read File", "read test.txt")
        ]
        
        for i, (text, cmd) in enumerate(quick_commands):
            btn = ttk.Button(
                quick_frame, 
                text=text, 
                command=lambda c=cmd: self.set_input_and_process(c)
            )
            btn.grid(row=0, column=i, padx=2)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        input_frame.columnconfigure(0, weight=1)
    
    def set_input_and_process(self, command):
        self.input_var.set(command)
        self.process_input()
    
    def process_input(self):
        user_input = self.input_var.get().strip()
        if not user_input:
            return
        
        self.append_output(f"You: {user_input}\n", "user")
        self.input_var.set("")
        
        # Process in background to avoid GUI freeze
        thread = threading.Thread(target=self.process_command_thread, args=(user_input,))
        thread.daemon = True
        thread.start()
    
    def process_command_thread(self, user_input):
        try:
            intent = self.brain.predict_intent(user_input)
            response = ""
            
            if intent['tag'] == 'greeting':
                response = "🚀 Hello! I'm Aetherium AI Assistant. How can I help you?"
            elif intent['tag'] == 'list_files':
                response = list_files()
            elif intent['tag'] == 'create_file':
                words = user_input.split()
                filename = next((word for word in words if '.' in word), "new_file.txt")
                response = create_file(filename, "Created by Aetherium")
            elif intent['tag'] == 'read_file':
                words = user_input.split()
                filename = next((word for word in words if '.' in word), None)
                response = read_file(filename) if filename else "Please specify a filename."
            elif intent['tag'] == 'delete_file':
                words = user_input.split()
                filename = next((word for word in words if '.' in word), None)
                response = delete_file(filename) if filename else "Please specify a filename."
            elif intent['tag'] == 'system_info':
                response = handle_system_command()
            elif intent['tag'] == 'run_command':
                words = user_input.split()
                command = " ".join(words[words.index('run')+1:] if 'run' in words else words[1:])
                response = execute_command(command) if command else "Please specify a command."
            else:
                response = intent['response']
            
            self.append_output(f"Aetherium: {response}\n\n", "ai")
            
        except Exception as e:
            self.append_output(f"❌ Error: {e}\n\n", "error")
    
    def append_output(self, text, text_type="normal"):
        def update_gui():
            self.output_text.configure(state='normal')
            
            if text_type == "user":
                self.output_text.insert(tk.END, text, "user")
            elif text_type == "ai":
                self.output_text.insert(tk.END, text, "ai")
            elif text_type == "error":
                self.output_text.insert(tk.END, text, "error")
            else:
                self.output_text.insert(tk.END, text)
            
            self.output_text.see(tk.END)
            self.output_text.configure(state='disabled')
        
        self.root.after(0, update_gui)

def start_gui():
    root = tk.Tk()
    app = AetheriumGUI(root)
    
    # Configure tags for colored text
    app.output_text.configure(state='normal')
    app.output_text.tag_configure("user", foreground="blue")
    app.output_text.tag_configure("ai", foreground="green")
    app.output_text.tag_configure("error", foreground="red")
    app.output_text.configure(state='disabled')
    
    root.mainloop()

if __name__ == "__main__":
    start_gui()