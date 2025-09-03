# powershell_data.py
import json

def create_powershell_training_data():
    """PowerShell command training data"""
    
    powershell_commands = {
        "ps_file_management": {
            "cmdlets": [
                "Get-ChildItem", "Set-Location", "Copy-Item", "Move-Item", 
                "Rename-Item", "Remove-Item", "New-Item", "Get-Content", 
                "Set-Content", "Test-Path"
            ],
            "patterns": [
                "powershell list files", "ps get child item", "powershell change directory",
                "ps copy file", "powershell move file", "ps rename file", "powershell delete file",
                "ps create file", "powershell read file", "ps write file", "powershell check path"
            ]
        },
        "ps_system_info": {
            "cmdlets": [
                "Get-ComputerInfo", "Get-Process", "Get-Service", "Get-HotFix",
                "Get-WindowsFeature", "Get-TimeZone"
            ],
            "patterns": [
                "powershell system info", "ps computer information", "powershell processes",
                "ps services", "powershell hotfix", "ps windows features", "powershell timezone"
            ]
        },
        "ps_network": {
            "cmdlets": [
                "Test-NetConnection", "Resolve-DnsName", "Get-NetIPConfiguration",
                "Get-NetAdapter", "Test-Connection"
            ],
            "patterns": [
                "powershell network test", "ps test connection", "powershell dns lookup",
                "ps ip configuration", "powershell network adapter", "ps ping"
            ]
        }
    }
    
    training_data = {"intents": []}
    
    for category, data in powershell_commands.items():
        intent = {
            "tag": category,
            "patterns": data["patterns"].copy(),
            "responses": [f"Executing PowerShell {category.replace('ps_', '').replace('_', ' ')}..."]
        }
        
        # Add cmdlet-specific patterns
        for cmdlet in data["cmdlets"]:
            intent["patterns"].extend([
                f"{cmdlet}",
                f"use {cmdlet}",
                f"powershell {cmdlet}",
                f"ps {cmdlet}",
                f"how to use {cmdlet}",
                f"what does {cmdlet} do"
            ])
        
        training_data["intents"].append(intent)
    
    return training_data

def save_powershell_data():
    data = create_powershell_training_data()
    
    with open("brain/data/powershell_commands.json", 'w') as f:
        json.dump(data, f, indent=2)
    
    total_patterns = sum(len(intent["patterns"]) for intent in data["intents"])
    print(f"✅ Created PowerShell training data with {len(data['intents'])} categories and {total_patterns} patterns")

if __name__ == "__main__":
    save_powershell_data()