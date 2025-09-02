import typer
from typing import Annotated, Optional, List
import sys
import os
from brain.data_generator import generate_training_data

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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

from config import APP_CONFIG, MODEL_CONFIG, COMMAND_CONFIG

app = typer.Typer(help=APP_CONFIG["description"])

brain = AetheriumBrain()
trainer = ModelTrainer(brain)

@app.command(name="generate-data")
def generate_data_command(
    overwrite: Annotated[bool, typer.Option(
        "--overwrite", "-o",
        help="Overwrite existing data files"
    )] = False
):
    """Generate training data for the AI model"""
    if not overwrite and (Path("brain/data/intents.json").exists() or 
                         Path("brain/data/vocab.json").exists()):
        if not typer.confirm("Data files already exist. Overwrite?"):
            print("❌ Data generation cancelled.")
            return
    
    generate_training_data()
    print("✅ Training data generated successfully!")
    print("💡 Now train the model with: python main.py train")

def process_command(user_input):
    intent = brain.predict_intent(user_input)
    
    if intent['tag'] == 'greeting':
        return "🚀 Hello! I'm Aetherium AI Assistant. How can I help you?"
    
    elif intent['tag'] == 'list_files':
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
        return read_file(filename) if filename else "Please specify a filename."
    
    elif intent['tag'] == 'delete_file':
        words = user_input.split()
        filename = next((word for word in words if '.' in word), None)
        return delete_file(filename) if filename else "Please specify a filename."
    
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
    
    elif intent['tag'] == 'run_command':
        words = user_input.split()
        command = " ".join(words[words.index('run')+1:] if 'run' in words else words[1:])
        return execute_command(command) if command else "Please specify a command."
    
    elif intent['tag'] == 'help':
        return "I can help with: files, system info, running commands, and more!"
    
    else:
        return intent['response']

@app.command(name="chat")
def chat_mode(
    message: Annotated[Optional[str], typer.Argument(help="Your message to Aetherium")] = None
):
    if message:
        response = process_command(message)
        print(f"🤖 {response}")
    else:
        print("💬 Aetherium Chat Mode (type 'exit', 'quit', or 'bye' to quit)")
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

@app.command(name="run")
def run_command(
    command: Annotated[str, typer.Argument(help="Command to execute")],
    args: Annotated[Optional[List[str]], typer.Argument(help="Command arguments")] = None
):
    full_command = f"{command} {' '.join(args) if args else ''}"
    result = execute_command(full_command)
    print(result)

@app.command(name="files")
def list_files_command(
    directory: Annotated[Optional[str], typer.Argument(help="Directory to list")] = "."
):
    result = list_files(directory)
    print(result)

@app.command(name="create")
def create_file_command(
    filename: Annotated[str, typer.Argument(help="Filename to create")],
    content: Annotated[Optional[str], typer.Option(help="File content")] = ""
):
    result = create_file(filename, content)
    print(result)

@app.command(name="read")
def read_file_command(
    filename: Annotated[str, typer.Argument(help="Filename to read")]
):
    result = read_file(filename)
    print(result)

@app.command(name="delete")
def delete_file_command(
    filename: Annotated[str, typer.Argument(help="Filename to delete")]
):
    result = delete_file(filename)
    print(result)

@app.command(name="system")
def system_info_command():
    result = handle_system_command()
    print(result)

@app.command(name="processes")
def processes_command():
    result = handle_process_list()
    print(result)

@app.command(name="disk")
def disk_info_command():
    result = handle_disk_usage()
    print(result)

@app.command(name="network")
def network_info_command():
    result = handle_network_info()
    print(result)

@app.command(name="uptime")
def uptime_command():
    result = handle_system_uptime()
    print(result)

@app.command(name="train")
def train_model(
    epochs: Annotated[int, typer.Option(help="Number of training epochs")] = MODEL_CONFIG["epochs"]
):
    print("🧠 Training Aetherium AI model...")
    trainer.train_model(epochs=epochs)
    print("✅ Training complete!")

@app.command(name="help")
def show_help():
    help_text = f"""
🎯 {APP_CONFIG['name']} v{APP_CONFIG['version']}

📋 Available Commands:
  chat [message]    - Chat with Aetherium AI
  run <command>     - Execute system command
  files [dir]       - List files in directory
  create <file>     - Create a new file
  read <file>       - Read file content
  delete <file>     - Delete a file
  system            - Show system information
  processes         - Show running processes
  disk              - Show disk usage
  network           - Show network information
  uptime            - Show system uptime
  train             - Train the AI model
  help              - Show this help
  gui               - Launch GUI interface

💬 Examples:
  aetherium chat "list files"
  aetherium run dir
  aetherium files C:\\
  aetherium create test.txt "Hello"
  aetherium system

🔧 AI Model: Custom Neural Network
"""
    print(help_text)

@app.command(name="gui")
def launch_gui():
    """Launch the GUI interface"""
    try:
        from gui import start_gui
        start_gui()
    except ImportError as e:
        print(f"❌ GUI not available: {e}")
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")

@app.command(name="version")
def show_version():
    """Show version information"""
    version_info = f"""
🤖 {APP_CONFIG['name']}
Version: {APP_CONFIG['version']}
Description: {APP_CONFIG['description']}
AI Model: Custom Neural Network
"""
    print(version_info)

if __name__ == "__main__":
    print(f"🚀 Starting {APP_CONFIG['name']} v{APP_CONFIG['version']}...")
    print("💡 Type 'help' to see available commands or 'chat' for interactive mode")
    app()