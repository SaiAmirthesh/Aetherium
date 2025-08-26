import typer
from typing import Annotated, Optional, List
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import from packages using the __init__.py structure
from brain import AetheriumBrain, ModelTrainer
from commands import (
    handle_system_command,
    handle_process_list,
    handle_disk_usage,
    handle_network_info,
    handle_system_uptime,
    list_files,
    create_file,
    read_file,
    delete_file,
    create_directory,
    delete_directory,
    execute_command,
    get_file_info,
    COMMAND_HANDLERS
)

app = typer.Typer(help="Aetherium - Your custom AI CLI assistant")

# Initialize the AI brain
brain = AetheriumBrain()
trainer = ModelTrainer(brain)

def process_command(user_input):
    """Process user input and return appropriate response"""
    intent = brain.predict_intent(user_input)
    
    # Handle different intents with enhanced capabilities
    if intent['tag'] == 'greeting':
        return "🚀 Hello! I'm Aetherium, your custom CLI assistant. How can I help you today?"
    
    elif intent['tag'] == 'list_files':
        # Extract directory from input if specified
        words = user_input.split()
        directory = next((word for word in words if os.path.isdir(word)), ".")
        return list_files(directory)
    
    elif intent['tag'] == 'create_file':
        words = user_input.split()
        filename = next((word for word in words if '.' in word), "new_file.txt")
        content = " ".join([word for word in words if word != filename and not word.startswith('create')])
        return create_file(filename, content)
    
    elif intent['tag'] == 'read_file':
        words = user_input.split()
        filename = next((word for word in words if '.' in word), None)
        if filename:
            return read_file(filename)
        else:
            return "Please specify a filename to read."
    
    elif intent['tag'] == 'delete_file':
        words = user_input.split()
        filename = next((word for word in words if '.' in word), None)
        if filename:
            return delete_file(filename)
        else:
            return "Please specify a filename to delete."
    
    elif intent['tag'] == 'system_info':
        return handle_system_command()
    
    elif intent['tag'] == 'process_list':
        return handle_process_list()
    
    elif intent['tag'] == 'disk_info':
        return handle_disk_usage()
    
    elif intent['tag'] == 'network_info':
        return handle_network_info()
    
    elif intent['tag'] == 'uptime':
        return handle_system_uptime()
    
    elif intent['tag'] == 'execute_command':
        # Extract command from input
        words = user_input.split()
        command = " ".join(words[words.index('run')+1:] if 'run' in words else words[1:])
        return execute_command(command) if command else "Please specify a command to execute."
    
    elif intent['tag'] == 'unknown':
        return intent['response']
    
    return "🤔 I'm not sure how to handle that command. Try 'help' to see available options."

@app.command(name="chat")
def chat_mode(
    message: Annotated[Optional[str], typer.Argument(help="Your message to Aetherium")] = None
):
    """Chat with Aetherium AI assistant"""
    if message:
        response = process_command(message)
        print(f"🤖 {response}")
    else:
        # Interactive mode
        print("💬 Aetherium Chat Mode (type 'exit', 'quit', or 'bye' to quit)")
        print("💡 Try: list files, system info, create file.txt, etc.")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    show_help()
                    continue
                
                if user_input:
                    response = process_command(user_input)
                    print(f"Aetherium: {response}")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

@app.command(name="run")
def run_command(
    command: Annotated[str, typer.Argument(help="Command to execute")],
    args: Annotated[Optional[List[str]], typer.Argument(help="Command arguments")] = None
):
    """Execute a system command"""
    full_command = f"{command} {' '.join(args) if args else ''}"
    result = execute_command(full_command)
    print(result)

@app.command(name="files")
def list_files_command(
    directory: Annotated[Optional[str], typer.Argument(help="Directory to list")] = "."
):
    """List files in directory"""
    result = list_files(directory)
    print(result)

@app.command(name="create")
def create_file_command(
    filename: Annotated[str, typer.Argument(help="Filename to create")],
    content: Annotated[Optional[str], typer.Option(help="File content")] = ""
):
    """Create a new file"""
    result = create_file(filename, content)
    print(result)

@app.command(name="read")
def read_file_command(
    filename: Annotated[str, typer.Argument(help="Filename to read")]
):
    """Read file content"""
    result = read_file(filename)
    print(result)

@app.command(name="delete")
def delete_file_command(
    filename: Annotated[str, typer.Argument(help="Filename to delete")]
):
    """Delete a file"""
    result = delete_file(filename)
    print(result)

@app.command(name="mkdir")
def create_dir_command(
    dirname: Annotated[str, typer.Argument(help="Directory name to create")]
):
    """Create a new directory"""
    result = create_directory(dirname)
    print(result)

@app.command(name="rmdir")
def delete_dir_command(
    dirname: Annotated[str, typer.Argument(help="Directory name to delete")]
):
    """Delete a directory"""
    result = delete_directory(dirname)
    print(result)

@app.command(name="system")
def system_info_command():
    """Show system information"""
    result = handle_system_command()
    print(result)

@app.command(name="processes")
def processes_command():
    """Show running processes"""
    result = handle_process_list()
    print(result)

@app.command(name="disk")
def disk_info_command():
    """Show disk usage"""
    result = handle_disk_usage()
    print(result)

@app.command(name="network")
def network_info_command():
    """Show network information"""
    result = handle_network_info()
    print(result)

@app.command(name="uptime")
def uptime_command():
    """Show system uptime"""
    result = handle_system_uptime()
    print(result)

@app.command(name="train")
def train_model(
    epochs: Annotated[int, typer.Option(help="Number of training epochs")] = 1000
):
    """Train the AI model"""
    print("🧠 Training Aetherium AI model...")
    trainer.train_model(epochs=epochs)
    print("✅ Training complete! The model has been saved.")

@app.command(name="help")
def show_help():
    """Show available commands and help"""
    help_text = """
🎯 Aetherium CLI Assistant - Your Custom AI Assistant

📋 Available Commands:

  chat [message]    - Chat with Aetherium AI (interactive mode)
  run <command>     - Execute system command
  files [dir]       - List files in directory
  create <file>     - Create a new file
  read <file>       - Read file content
  delete <file>     - Delete a file
  mkdir <dir>       - Create a new directory
  rmdir <dir>       - Delete a directory
  system            - Show system information
  processes         - Show running processes
  disk              - Show disk usage
  network           - Show network information
  uptime            - Show system uptime
  train             - Train the AI model
  help              - Show this help message

💬 Chat Examples:
  aetherium chat "hello"
  aetherium chat "list files in C:\\Users"
  aetherium chat "create test.txt with some content"
  aetherium chat "show system info"
  aetherium chat "what processes are running?"

⚡ Direct Command Examples:
  aetherium run dir /w
  aetherium files C:\\
  aetherium create example.txt "Hello World"
  aetherium read example.txt
  aetherium system
  aetherium processes

🔧 Technical:
  Model: Custom Neural Network
  Version: 1.0.0
  No external API dependencies!
"""
    print(help_text)

@app.command(name="version")
def show_version():
    """Show Aetherium version"""
    version_info = """
🤖 Aetherium CLI Assistant
Version: 1.0.0
Author: Custom Built
Description: Self-contained AI assistant without external APIs
Features: Neural Network AI, File Operations, System Monitoring
"""
    print(version_info)

@app.callback()
def main():
    """Aetherium - Your custom AI CLI assistant built from scratch"""
    pass

if __name__ == "__main__":
    print("🚀 Starting Aetherium CLI Assistant...")
    print("💡 Type 'help' to see available commands or 'chat' for interactive mode")
    app()