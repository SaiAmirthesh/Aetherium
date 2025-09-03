# windows_admin_commands.py
import json

def create_admin_training_data():
    """Windows administrative commands training data"""
    
    admin_commands = {
        "windows_administration": {
            "commands": [
                "sfc", "chkdsk", "dism", "gpupdate", "gpresult", "netstat",
                "sc", "reg", "bcdedit", "powercfg", "systeminfo", "tasklist"
            ],
            "patterns": [
                "system file checker", "check system files", "disk check",
                "deployment image", "group policy update", "group policy result",
                "network statistics", "service control", "registry editor",
                "boot configuration", "power configuration", "system information",
                "task list", "windows admin", "system administration"
            ]
        },
        "windows_troubleshooting": {
            "commands": [
                "ping", "tracert", "ipconfig", "netstat", "nslookup", "pathping",
                "arp", "route", "netsh"
            ],
            "patterns": [
                "network troubleshooting", "ping test", "trace route",
                "ip configuration", "network stats", "dns lookup",
                "path ping", "address resolution", "network routing",
                "network shell", "troubleshoot network", "fix network"
            ]
        },
        "windows_security": {
            "commands": [
                "whoami", "net user", "net localgroup", "icacls", "cacls",
                "takeown", "attrib"
            ],
            "patterns": [
                "security commands", "user permissions", "file permissions",
                "take ownership", "file attributes", "access control",
                "user management", "group management", "windows security"
            ]
        }
    }
    
    training_data = {"intents": []}
    
    for category, data in admin_commands.items():
        intent = {
            "tag": category,
            "patterns": data["patterns"].copy(),
            "responses": [f"Executing Windows {category.replace('windows_', '').replace('_', ' ')} command..."]
        }
        
        # Add command-specific patterns
        for command in data["commands"]:
            intent["patterns"].extend([
                f"{command}",
                f"use {command}",
                f"run {command}",
                f"windows {command}",
                f"admin {command}",
                f"how to use {command}",
                f"troubleshoot with {command}"
            ])
        
        training_data["intents"].append(intent)
    
    return training_data

def save_admin_data():
    data = create_admin_training_data()
    
    with open("brain/data/windows_admin_commands.json", 'w') as f:
        json.dump(data, f, indent=2)
    
    total_patterns = sum(len(intent["patterns"]) for intent in data["intents"])
    print(f"✅ Created Windows admin training data with {len(data['intents'])} categories and {total_patterns} patterns")

if __name__ == "__main__":
    save_admin_data()