import os
import subprocess
from pathlib import Path
import shutil

def list_files(directory="."):
    try:
        if not os.path.exists(directory):
            return f"❌ Directory '{directory}' does not exist"
        
        files = os.listdir(directory)
        if not files:
            return "📁 Directory is empty"
        
        result = []
        for file in files:
            full_path = os.path.join(directory, file)
            if os.path.isdir(full_path):
                result.append(f"📁 {file}/")
            else:
                size = os.path.getsize(full_path)
                result.append(f"📄 {file} ({size} bytes)")
        
        return "\n".join(result)
    
    except PermissionError:
        return "❌ Permission denied to access directory"
    except Exception as e:
        return f"❌ Error: {e}"

def create_file(filename, content=""):
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return f"✅ Created file: {filename}"
    except Exception as e:
        return f"❌ Error creating file: {e}"

def read_file(filename):
    try:
        if not os.path.exists(filename):
            return f"❌ File '{filename}' does not exist"
        
        with open(filename, 'r') as f:
            content = f.read()
        
        if not content:
            return "📄 File is empty"
        
        return f"Content of {filename}:\n{content}"
    
    except Exception as e:
        return f"❌ Error reading file: {e}"

def delete_file(filename):
    try:
        if not os.path.exists(filename):
            return f"❌ File '{filename}' does not exist"
        
        os.remove(filename)
        return f"✅ Deleted file: {filename}"
    
    except Exception as e:
        return f"❌ Error deleting file: {e}"

def create_directory(dirname):
    try:
        os.makedirs(dirname, exist_ok=True)
        return f"✅ Created directory: {dirname}"
    except Exception as e:
        return f"❌ Error creating directory: {e}"

def delete_directory(dirname):
    try:
        if not os.path.exists(dirname):
            return f"❌ Directory '{dirname}' does not exist"
        
        shutil.rmtree(dirname)
        return f"✅ Deleted directory: {dirname}"
    
    except Exception as e:
        return f"❌ Error deleting directory: {e}"

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            return result.stdout if result.stdout else "✅ Command executed successfully"
        else:
            return f"❌ Command failed:\n{result.stderr}"
    
    except subprocess.TimeoutExpired:
        return "❌ Command timed out after 30 seconds"
    except Exception as e:
        return f"❌ Error executing command: {e}"

def get_file_info(filename):
    try:
        if not os.path.exists(filename):
            return f"❌ File '{filename}' does not exist"
        
        stat = os.stat(filename)
        info = {
            "Name": filename,
            "Size": f"{stat.st_size} bytes",
            "Created": f"{stat.st_ctime}",
            "Modified": f"{stat.st_mtime}",
            "Is Directory": os.path.isdir(filename),
            "Is File": os.path.isfilename(filename)
        }
        
        return "\n".join([f"{k}: {v}" for k, v in info.items()])
    
    except Exception as e:
        return f"❌ Error getting file info: {e}"