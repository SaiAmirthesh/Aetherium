# ⚡ Aetherium AI Assistant

A powerful AI-powered CLI and GUI assistant with custom neural network capabilities, designed for Windows command management and system administration.

## 🚀 Features

### Core AI Capabilities
- **Custom Neural Network**: Built-in AI model for intelligent command recognition
- **Natural Language Processing**: Understand commands in plain English
- **Intent Recognition**: Automatically detects user intent from natural language
- **Learning Capabilities**: Can be trained on custom datasets

### System Management
- **System Information**: Complete system specs, hardware info, and status
- **Process Management**: View running processes, system tasks, and performance
- **Network Tools**: IP configuration, network status, connection testing
- **Disk Management**: Storage usage, disk health, and space monitoring
- **User Management**: Logged-in users, user accounts, and permissions
- **Service Management**: Windows services status and management
- **Environment Variables**: System and user environment configuration

### File Operations
- **File Listing**: Directory browsing with detailed file information
- **File Creation**: Create new files with custom content
- **File Reading**: View file contents and metadata
- **File Deletion**: Safe file removal with confirmation
- **Directory Management**: Create and remove directories
- **File Information**: Detailed file properties and statistics

### Command Execution
- **System Commands**: Execute Windows commands and PowerShell cmdlets
- **Batch Operations**: Run multiple commands in sequence
- **Command History**: Track and repeat previous commands
- **Error Handling**: Comprehensive error reporting and recovery

## 🛠️ Installation

### Prerequisites
- Python 3.7+
- Windows 10/11 (primary target)
- PowerShell (for advanced features)

### Quick Setup
```bash
# Clone the repository
git clone <repository-url>
cd Aetherium

# Install dependencies
python setup.py

# Generate training data
python main.py generate-data

# Train the AI model
python main.py train
```

### Manual Installation
```bash
# Install required packages
pip install typer numpy psutil

# Generate training data
python brain/data_generator.py

# Merge Windows command data
python windows_data_merger.py
```

## 📖 Usage

### CLI Mode
```bash
# Interactive chat mode
python main.py chat

# Direct command execution
python main.py chat "list files"

# System information
python main.py system

# Process management
python main.py processes

# Network information
python main.py network

# Disk usage
python main.py disk

# System uptime
python main.py uptime

# User management
python main.py users

# Environment variables
python main.py env

# Service management
python main.py services

# File operations
python main.py files [directory]
python main.py create <filename> [content]
python main.py read <filename>
python main.py delete <filename>

# Execute custom commands
python main.py run <command>
```

### GUI Mode
```bash
# Launch graphical interface
python main.py gui
```

The GUI provides:
- **Command Input**: Natural language command entry
- **Quick Actions**: One-click access to common operations
- **Real-time Output**: Live command execution results
- **Visual Feedback**: Color-coded responses and status indicators

### Chat Mode Examples
```
You: hello
Aetherium: 🚀 Hello! I'm Aetherium AI Assistant. How can I help you today?

You: show me my files
Aetherium: 📁 Listing files in the current directory...

You: what's my system info?
Aetherium: 🖥️ Gathering system information...

You: check disk space
Aetherium: 💾 Checking disk usage...

You: who is logged in?
Aetherium: 👥 Showing logged in users...

You: show running services
Aetherium: 🔧 Checking running services...

You: create a test file
Aetherium: 📝 Creating a new file...
```

## 🧠 AI Model

### Architecture
- **Input Layer**: Vocabulary-based text vectorization
- **Hidden Layer**: 8 neurons with sigmoid activation
- **Output Layer**: Intent classification with confidence scoring
- **Training**: Backpropagation with customizable learning rate

### Training Data
- **Windows Commands**: Comprehensive CMD and PowerShell patterns
- **System Administration**: Administrative and troubleshooting commands
- **File Operations**: File and directory management patterns
- **Natural Language**: Human-readable command variations

### Customization
```python
# Train with custom data
from brain import ModelTrainer
trainer = ModelTrainer(brain)
trainer.train_model(epochs=2000, learning_rate=0.05)

# Add custom intents
brain.intents.append({
    "tag": "custom_operation",
    "patterns": ["custom command", "special operation"],
    "responses": ["Executing custom operation..."]
})
```

## 🔧 Configuration

### Model Settings
```python
# config.py
MODEL_CONFIG = {
    "input_size": 50,
    "hidden_size": 8,
    "output_size": 10,
    "learning_rate": 0.1,
    "epochs": 1000
}
```

### GUI Theme
```python
# config.py
GUI_CONFIG = {
    "theme": "dark",
    "window_size": "800x600",
    "font_family": "Arial",
    "font_size": 10
}
```

### Command Security
```python
# config.py
COMMAND_CONFIG = {
    "safe_mode": True,
    "confirm_destructive_actions": True,
    "allowed_commands": ["dir", "systeminfo", "tasklist"]
}
```

## 📁 Project Structure
```
Aetherium/
├── brain/                   # AI core components
│   ├── __init__.py
│   ├── model.py            # Neural network implementation
│   ├── trainer.py          # Model training logic
│   ├── data_generator.py   # Training data generation
│   ├── data/               # Training datasets
│   └── models/             # Saved AI models
├── commands/                # Command implementations
│   ├── __init__.py
│   ├── system.py           # System management commands
│   └── file_ops.py         # File operation commands
├── main.py                  # CLI entry point
├── gui.py                   # GUI implementation
├── config.py                # Configuration settings
├── setup.py                 # Installation script
├── test_features.py         # Feature testing
└── README.md               # This file
```

## 🧪 Testing

### Run All Tests
```bash
python test_features.py
```

### Test Specific Features
```bash
# Test CLI
python main.py help

# Test GUI
python main.py gui

# Test AI model
python -c "from brain import AetheriumBrain; brain = AetheriumBrain(); print(brain.predict_intent('hello'))"
```

## 🚨 Troubleshooting

### Common Issues

**Import Errors**
```bash
# Ensure proper Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
# or
python -m pip install -e .
```

**Missing Dependencies**
```bash
# Install required packages
pip install -r requirements.txt
```

**Model Training Issues**
```bash
# Regenerate training data
python main.py generate-data --overwrite

# Retrain model
python main.py train
```

**Permission Errors**
- Run as Administrator for system-level operations
- Check file/directory permissions
- Ensure PowerShell execution policy allows scripts

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test individual components
from brain import AetheriumBrain
brain = AetheriumBrain()
print(f"Vocabulary size: {len(brain.vocab)}")
print(f"Intents: {[i['tag'] for i in brain.intents]}")
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests for new features
5. Submit a pull request

### Adding New Commands
```python
# commands/new_feature.py
def handle_new_feature():
    """Handle new feature command"""
    try:
        # Implementation here
        return "✅ Feature executed successfully"
    except Exception as e:
        return f"❌ Error: {e}"

# commands/__init__.py
from .new_feature import handle_new_feature
COMMAND_HANDLERS['new_feature'] = handle_new_feature
```

### Adding New Intents
```python
# brain/data_generator.py
"new_intent": {
    "patterns": ["new command", "new operation"],
    "responses": ["Executing new operation..."]
}
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Neural Network Implementation**: Custom implementation for educational purposes
- **Windows Commands**: Comprehensive Windows command reference
- **GUI Framework**: Tkinter for cross-platform compatibility
- **CLI Framework**: Typer for modern command-line interfaces

## 📞 Support

- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: Check the wiki for detailed guides
- **Community**: Join discussions in the community forum

---

**⚡ Aetherium AI Assistant** - Empowering users with intelligent system management through AI-powered natural language commands.
