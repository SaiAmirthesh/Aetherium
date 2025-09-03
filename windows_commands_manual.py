# windows_commands_manual.py
import json

def create_windows_training_data():
    """Manual collection of real Windows commands with patterns"""
    
    windows_commands = {
        "file_management": {
            "commands": [
                "dir", "cd", "copy", "xcopy", "move", "ren", "rename", 
                "del", "erase", "mkdir", "md", "rmdir", "rd", "tree", 
                "type", "more", "find", "findstr", "sort"
            ],
            "patterns": [
                "list files", "show directory", "display files", "change directory",
                "copy file", "move file", "rename file", "delete file", "remove file",
                "create directory", "make folder", "remove directory", "show folder tree",
                "display file content", "view file", "search in files", "sort files"
            ]
        },
        "system_info": {
            "commands": [
                "systeminfo", "hostname", "ver", "winver", "whoami", "time", 
                "date", "echo", "set", "path"
            ],
            "patterns": [
                "system information", "computer info", "system specs", "hostname",
                "windows version", "who am i", "current time", "current date",
                "display message", "environment variables", "set path"
            ]
        },
        "network_commands": {
            "commands": [
                "ipconfig", "ping", "tracert", "pathping", "netstat", "nslookup",
                "netsh", "getmac", "arp"
            ],
            "patterns": [
                "ip configuration", "network configuration", "ping address",
                "trace route", "network statistics", "dns lookup", "network shell",
                "mac address", "arp table", "check connection", "test network"
            ]
        },
        "process_management": {
            "commands": [
                "tasklist", "taskkill", "start", "schtasks", "timeout"
            ],
            "patterns": [
                "list processes", "running tasks", "kill process", "end task",
                "start program", "schedule task", "wait timeout", "show tasks"
            ]
        },
        "disk_management": {
            "commands": [
                "chkdsk", "format", "diskpart", "vol", "label"
            ],
            "patterns": [
                "check disk", "disk check", "format disk", "disk partition",
                "volume info", "disk label", "drive information"
            ]
        },
        "power_management": {
            "commands": [
                "shutdown", "powercfg", "logoff"
            ],
            "patterns": [
                "shutdown computer", "restart computer", "power configuration",
                "log off", "sign out", "power options", "energy settings"
            ]
        },
        "user_management": {
            "commands": [
                "net user", "net localgroup", "whoami"
            ],
            "patterns": [
                "user accounts", "manage users", "user groups", "local groups",
                "current user", "user information", "create user", "delete user"
            ]
        },
        "batch_scripting": {
            "commands": [
                "call", "goto", "if", "for", "choice", "pause", "exit"
            ],
            "patterns": [
                "batch script", "call function", "goto label", "if condition",
                "for loop", "user choice", "pause script", "exit program"
            ]
        }
    }
    
    training_data = {"intents": []}
    
    for category, data in windows_commands.items():
        intent = {
            "tag": category,
            "patterns": [],
            "responses": [f"Executing {category.replace('_', ' ')} command..."]
        }
        
        # Add category patterns
        intent["patterns"].extend(data["patterns"])
        
        # Add command-specific patterns
        for command in data["commands"]:
            intent["patterns"].extend([
                f"{command}",
                f"use {command}",
                f"run {command}",
                f"execute {command}",
                f"{command} command",
                f"how to use {command}",
                f"what does {command} do",
                f"windows {command}",
                f"cmd {command}"
            ])
        
        training_data["intents"].append(intent)
    
    return training_data

def save_windows_data():
    data = create_windows_training_data()
    
    with open("brain/data/real_windows_commands.json", 'w') as f:
        json.dump(data, f, indent=2)
    
    total_patterns = sum(len(intent["patterns"]) for intent in data["intents"])
    print(f"✅ Created training data with {len(data['intents'])} categories and {total_patterns} patterns")

if __name__ == "__main__":
    save_windows_data()