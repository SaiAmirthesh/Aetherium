# windows_data_merger.py
import json
from pathlib import Path

def merge_windows_data():
    """Merge all Windows command training data"""
    data_files = [
        "brain/data/real_windows_commands.json",
        "brain/data/powershell_commands.json",
        "brain/data/windows_admin_commands.json"
    ]
    
    merged_data = {"intents": []}
    
    for file_path in data_files:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    merged_data["intents"].extend(data["intents"])
            except Exception as e:
                print(f"⚠️  Error loading {file_path}: {e}")
    
    # Save merged data
    with open("brain/data/combined_windows_commands.json", 'w') as f:
        json.dump(merged_data, f, indent=2)
    
    total_patterns = sum(len(intent["patterns"]) for intent in merged_data["intents"])
    print(f"✅ Merged {len(merged_data['intents'])} Windows command categories with {total_patterns} patterns")
    
    return merged_data

if __name__ == "__main__":
    merge_windows_data()