"""
Aetherium Configuration
"""

# AI Model Configuration
MODEL_CONFIG = {
    "input_size": 50,
    "hidden_size": 8,
    "output_size": 10,
    "learning_rate": 0.1,
    "epochs": 1000,
    "model_path": "brain/models/aetherium_model.npy",
    "vocab_path": "brain/data/vocab.json",
    "intents_path": "brain/data/intents.json"
}

# Application Configuration
APP_CONFIG = {
    "name": "Aetherium AI Assistant",
    "version": "1.0.0",
    "description": "Custom AI-powered CLI and GUI assistant",
    "default_model": "aetherium_model",
    "max_history": 1000,
    "log_file": "aetherium.log"
}

# GUI Configuration
GUI_CONFIG = {
    "window_title": "Aetherium AI Assistant",
    "window_size": "800x600",
    "theme": "dark",
    "font_family": "Arial",
    "font_size": 10,
    "max_display_lines": 1000
}

# Command Configuration
COMMAND_CONFIG = {
    "timeout": 30,
    "confirm_destructive_actions": True,
    "safe_mode": True,
    "allowed_commands": [
        "dir", "ls", "cd", "pwd", "echo", "type", 
        "mkdir", "rmdir", "copy", "move", "ren",
        "python", "pip", "git"
    ]
}
