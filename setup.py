import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    requirements = [
        "typer",
        "numpy",
        "psutil"
    ]
    
    print("📦 Installing dependencies...")
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Installed {package}")
        except:
            print(f"❌ Failed to install {package}")

def create_project_structure():
    directories = [
        "brain",
        "brain/data",
        "brain/models",
        "commands"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def generate_training_data():
    """Generate initial training data using the data generator"""
    try:
        # Add the current directory to Python path
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from brain.data_generator import generate_training_data as generate_data
        generate_data()
        print("✅ Generated comprehensive training data")
    except ImportError as e:
        print(f"❌ Could not import data generator: {e}")
        # Create minimal data as fallback
        create_minimal_data()
    except Exception as e:
        print(f"❌ Error generating training data: {e}")
        create_minimal_data()

def create_minimal_data():
    """Create minimal training data as fallback"""
    minimal_data = {
        "intents": [
            {
                "tag": "greeting",
                "patterns": ["hello", "hi", "hey"],
                "responses": ["Hello! How can I help you?"]
            },
            {
                "tag": "list_files",
                "patterns": ["list files", "show files", "dir"],
                "responses": ["Listing files..."]
            }
        ]
    }
    
    data_path = Path("brain/data/intents.json")
    data_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(data_path, 'w') as f:
        json.dump(minimal_data, f, indent=2)
    
    print("✅ Created minimal training data as fallback")

if __name__ == "__main__":
    print("🚀 Setting up Aetherium AI Assistant...")
    install_requirements()
    create_project_structure()
    generate_training_data()
    print("\n🎉 Setup complete! You can now:")
    print("  • Run CLI: python main.py help")
    print("  • Run GUI: python main.py gui")
    print("  • Train model: python main.py train")