import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
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
    """Create necessary directories"""
    directories = [
        "brain",
        "brain/data",
        "brain/models",
        "commands"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

if __name__ == "__main__":
    print("🚀 Setting up Aetherium CLI Assistant...")
    install_requirements()
    create_project_structure()
    print("🎉 Setup complete! Run: python main.py help")