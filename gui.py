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
        self.root.configure(bg='#000000')  # Black background
        
        # Set Aetherium theme colors
        self.colors = {
            'background': '#000000',      # Black
            'foreground': '#FFFFFF',      # White text
            'accent': '#8A2BE2',         # Purple - Aetherium color
            'secondary': '#4B0082',      # Dark purple
            'input_bg': '#1A1A1A',       # Dark gray input
            'text_bg': '#0D0D0D',        # Very dark gray text area
            'button_bg': '#8A2BE2',      # Purple buttons
            'button_fg': '#FFFFFF',      # White button text
            'button_active': '#6A0DAD',  # Darker purple when pressed
        }
        
        self.brain = AetheriumBrain()
        self.setup_gui()
        self.apply_theme()
    
    def apply_theme(self):
        """Apply the Aetherium color theme to all widgets"""
        style = ttk.Style()
        
        # Configure styles
        style.configure(
            'TFrame',
            background=self.colors['background']
        )
        
        style.configure(
            'TLabel',
            background=self.colors['background'],
            foreground=self.colors['foreground'],
            font=('Arial', 10)
        )
        
        style.configure(
            'TButton',
            background=self.colors['button_bg'],
            foreground=self.colors['button_fg'],
            borderwidth=0,
            focuscolor=self.colors['background']
        )
        
        style.map(
            'TButton',
            background=[('active', self.colors['button_active'])],
            foreground=[('active', self.colors['foreground'])]
        )
        
        style.configure(
            'TEntry',
            fieldbackground=self.colors['input_bg'],
            foreground=self.colors['foreground'],
            borderwidth=1,
            relief='flat'
        )
    
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.configure(style='TFrame')
        
        # Title with Aetherium purple
        title_label = tk.Label(
            main_frame, 
            text=f"⚡ AETHERIUM AI ASSISTANT",
            font=("Arial", 18, "bold"),
            fg=self.colors['accent'],    # Purple
            bg=self.colors['background'], # Black
            pady=10
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Subtitle
        subtitle_label = tk.Label(
            main_frame,
            text=f"Version {APP_CONFIG['version']} - Custom Neural Network AI",
            font=("Arial", 9),
            fg=self.colors['foreground'], # White
            bg=self.colors['background']  # Black
        )
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Input label
        input_label = tk.Label(
            input_frame, 
            text="Enter your command:",
            font=("Arial", 10, "bold"),
            fg=self.colors['accent'],    # Purple
            bg=self.colors['background'] # Black
        )
        input_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Input entry with custom styling
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(
            input_frame, 
            textvariable=self.input_var, 
            width=55,
            font=("Consolas", 10),
            bg=self.colors['input_bg'],   # Dark gray
            fg=self.colors['foreground'], # White
            insertbackground=self.colors['accent'],  # Purple cursor
            relief='flat',
            borderwidth=2
        )
        self.input_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.input_entry.bind('<Return>', lambda e: self.process_input())
        self.input_entry.bind('<Control-a>', lambda e: self.input_entry.select_range(0, tk.END))
        
        # Process button with purple theme
        self.process_btn = tk.Button(
            input_frame, 
            text="🚀 PROCESS",
            command=self.process_input,
            font=("Arial", 10, "bold"),
            bg=self.colors['button_bg'],      # Purple
            fg=self.colors['button_fg'],      # White
            activebackground=self.colors['button_active'],  # Darker purple
            activeforeground=self.colors['foreground'],     # White
            relief='flat',
            borderwidth=0,
            padx=15,
            pady=5
        )
        self.process_btn.grid(row=1, column=1)
        
        # Output area label
        output_label = tk.Label(
            main_frame, 
            text="AI RESPONSE:",
            font=("Arial", 10, "bold"),
            fg=self.colors['accent'],    # Purple
            bg=self.colors['background'] # Black
        )
        output_label.grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        
        # Output text area with dark theme
        self.output_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("Consolas", 9),
            bg=self.colors['text_bg'],    # Very dark gray
            fg=self.colors['foreground'], # White
            insertbackground=self.colors['accent'],  # Purple cursor
            relief='flat',
            borderwidth=2
        )
        self.output_text.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))
        
        # Quick buttons frame
        quick_frame = tk.Frame(main_frame, bg=self.colors['background'])
        quick_frame.grid(row=5, column=0, columnspan=2, pady=(20, 10))
        
        quick_commands = [
            ("📁 LIST FILES", "list files"),
            ("🖥️ SYSTEM INFO", "system info"),
            ("⚡ PROCESSES", "running processes"),
            ("💾 DISK USAGE", "disk usage"),
            ("📝 CREATE FILE", "create test.txt"),
            ("👁️ READ FILE", "read test.txt"),
            ("🌐 NETWORK", "network information"),
            ("⏰ UPTIME", "system uptime")
        ]
        
        for i, (text, cmd) in enumerate(quick_commands):
            btn = tk.Button(
                quick_frame, 
                text=text, 
                command=lambda c=cmd: self.set_input_and_process(c),
                font=("Arial", 8, "bold"),
                bg=self.colors['button_bg'],
                fg=self.colors['button_fg'],
                activebackground=self.colors['button_active'],
                activeforeground=self.colors['foreground'],
                relief='flat',
                padx=8,
                pady=4
            )
            btn.grid(row=0, column=i, padx=2)
        
        # Status bar
        status_bar = tk.Label(
            main_frame,
            text="🟢 Ready - Type a command or click quick actions above",
            font=("Arial", 8),
            fg=self.colors['accent'],
            bg=self.colors['background'],
            pady=5
        )
        status_bar.grid(row=6, column=0, columnspan=2, pady=(15, 0))
        
        # Configure grid weights for responsive layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        input_frame.columnconfigure(0, weight=1)
        
        # Focus on input field
        self.input_entry.focus()
        
        # Add welcome message
        self.append_output("⚡ AETHERIUM AI ASSISTANT INITIALIZED\n", "title")
        self.append_output("Version 1.0.0 - Custom Neural Network\n", "subtitle")
        self.append_output("\n💡 Type commands like:\n", "ai")
        self.append_output("  • 'list files' - Show directory contents\n", "ai")
        self.append_output("  • 'system info' - Display system information\n", "ai")
        self.append_output("  • 'create filename.txt' - Create a new file\n", "ai")
        self.append_output("  • 'run command' - Execute system commands\n\n", "ai")
        self.append_output("🚀 Ready to assist you!\n", "accent")
    
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
                response = "🚀 Hello! I'm Aetherium AI Assistant. How can I help you today?"
            elif intent['tag'] == 'list_files':
                response = list_files()
            elif intent['tag'] == 'create_file':
                words = user_input.split()
                filename = next((word for word in words if '.' in word), "new_file.txt")
                response = create_file(filename, "Created by Aetherium AI")
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
            
            # Configure tags for different text colors
            if not hasattr(self, 'tags_configured'):
                self.output_text.tag_configure("user", foreground="#FF6B9D")  # Pink for user
                self.output_text.tag_configure("ai", foreground="#00FFAA")    # Green for AI
                self.output_text.tag_configure("error", foreground="#FF5555") # Red for errors
                self.output_text.tag_configure("title", foreground=self.colors['accent'], font=("Arial", 12, "bold"))
                self.output_text.tag_configure("subtitle", foreground=self.colors['accent'], font=("Arial", 9))
                self.output_text.tag_configure("accent", foreground=self.colors['accent'])
                self.tags_configured = True
            
            if text_type == "user":
                self.output_text.insert(tk.END, text, "user")
            elif text_type == "ai":
                self.output_text.insert(tk.END, text, "ai")
            elif text_type == "error":
                self.output_text.insert(tk.END, text, "error")
            elif text_type == "title":
                self.output_text.insert(tk.END, text, "title")
            elif text_type == "subtitle":
                self.output_text.insert(tk.END, text, "subtitle")
            elif text_type == "accent":
                self.output_text.insert(tk.END, text, "accent")
            else:
                self.output_text.insert(tk.END, text)
            
            self.output_text.see(tk.END)
            self.output_text.configure(state='disabled')
        
        self.root.after(0, update_gui)

def start_gui():
    root = tk.Tk()
    root.title("Aetherium AI Assistant")
    root.geometry("900x700")
    root.configure(bg='#000000')
    
    # Set window icon (optional - you can add an icon file later)
    try:
        root.iconbitmap('aetherium.ico')  # If you have an icon file
    except:
        pass
    
    # Center the window on screen
    root.eval('tk::PlaceWindow . center')
    
    app = AetheriumGUI(root)
    root.mainloop()

if __name__ == "__main__":
    start_gui()