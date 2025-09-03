import json
import random
from pathlib import Path

class TrainingDataGenerator:
    def __init__(self):
        self.base_intents = {
            "greeting": {
                "patterns": [
                    "hello", "hi", "hey", "greetings", "howdy", "good morning",
                    "good afternoon", "good evening", "what's up", "yo"
                ],
                "responses": [
                    "Hello! How can I help you today?",
                    "Hi there! What can I do for you?",
                    "Hey! Ready to assist you.",
                    "Greetings! How may I help you?"
                ]
            },
            "list_files": {
                "patterns": [
                    "list files", "show files", "display files", "directory contents",
                    "folder contents", "ls", "dir", "list directory", "what files are here"
                ],
                "responses": ["Listing files in the current directory..."]
            },
            "create_file": {
                "patterns": [
                    "create file", "make file", "new file", "touch file",
                    "create a file", "make a new file", "create text file"
                ],
                "responses": ["Creating a new file..."]
            },
            "read_file": {
                "patterns": [
                    "read file", "open file", "view file", "show file content",
                    "display file", "cat file", "type file", "read document"
                ],
                "responses": ["Reading file contents..."]
            },
            "delete_file": {
                "patterns": [
                    "delete file", "remove file", "rm file", "del file",
                    "erase file", "delete a file", "remove a file"
                ],
                "responses": ["Deleting file..."]
            },
            "system_info": {
                "patterns": [
                    "system information", "system status", "computer info",
                    "show system", "system health", "hardware info"
                ],
                "responses": ["Gathering system information..."]
            },
            "process_list": {
                "patterns": [
                    "running processes", "show processes", "task list",
                    "what's running", "current processes", "process manager"
                ],
                "responses": ["Listing running processes..."]
            },
            "disk_usage": {
                "patterns": [
                    "disk usage", "storage info", "disk space", "free space",
                    "check disk", "disk information", "storage usage"
                ],
                "responses": ["Checking disk usage..."]
            },
            "network_info": {
                "patterns": [
                    "network information", "network status", "ip address",
                    "network config", "show network", "connection info"
                ],
                "responses": ["Gathering network information..."]
            },
            "run_command": {
                "patterns": [
                    "run command", "execute command", "run program",
                    "execute program", "run script", "execute script"
                ],
                "responses": ["Executing command..."]
            },
            "help": {
                "patterns": [
                    "help", "assist", "support", "how to", "what can you do",
                    "help me", "need help", "show help"
                ],
                "responses": ["I'm here to help! I can assist with files, system commands, and more."]
            },
            "python": {
                "patterns": [
                    "python script", "run python", "execute code",
                    "python code", "run script", "execute python"
                ],
                "responses": ["Running Python code..."]
            },
            "git": {
                "patterns": [
                    "git command", "version control", "clone repo",
                    "git status", "git commit", "git push"
                ],
                "responses": ["Git operations..."]
            },
            "list_files": {
                "patterns": [
                    "list files", "show files", "display files", "what files are here",
                    "directory contents", "folder contents", "ls", "dir", "list directory",
                    "show me the files", "what's in this folder", "display directory",
                    "list all files", "show contents", "view files", "see files",
                    "browse files", "explore directory", "what files do I have"
                ],
                "responses": ["Listing files in the current directory..."]
            },
            "system_info": {
                "patterns": [
                    "system information", "system status", "computer info",
                    "show system", "system health", "hardware info", "system specs",
                    "computer specifications", "what's my system", "system details",
                    "show computer info", "display system information", "my system specs"
                ],
                "responses": ["Gathering system information..."]
            }
        }
    
    def generate_variations(self, base_patterns):
        variations = set()
        
        for pattern in base_patterns:
            # Basic variations
            variations.add(pattern)
            variations.add(pattern + " please")
            variations.add("can you " + pattern)
            variations.add("how to " + pattern)
            variations.add("I want to " + pattern)
            variations.add("show me how to " + pattern)
            variations.add("help me " + pattern)
            variations.add("please " + pattern)
            variations.add("could you " + pattern)
            variations.add("would you " + pattern)
            
            # Question forms
            variations.add("what is " + pattern)
            variations.add("how do I " + pattern)
            variations.add("how can I " + pattern)
            
            # With different punctuation
            variations.add(pattern + "?")
            variations.add(pattern + "!")
            
            # Capitalized
            variations.add(pattern.capitalize())
        
        return list(variations)
    
    def generate_contextual_patterns(self):
        """Generate patterns with file extensions and common contexts"""
        contextual_patterns = {}
        
        file_extensions = [".txt", ".py", ".js", ".html", ".css", ".json", ".csv"]
        common_filenames = ["test", "file", "document", "data", "script", "config"]
        
        for tag, data in self.base_intents.items():
            if any(keyword in tag for keyword in ["file", "python", "script"]):
                enhanced_patterns = []
                for pattern in data["patterns"]:
                    # Add patterns with file extensions
                    for ext in file_extensions:
                        enhanced_patterns.append(pattern + ext)
                        enhanced_patterns.append(pattern + " " + random.choice(common_filenames) + ext)
                    
                    # Add patterns with specific filenames
                    for name in common_filenames:
                        enhanced_patterns.append(pattern + " " + name)
                        enhanced_patterns.append(pattern + " " + name + ".txt")
                
                contextual_patterns[tag] = enhanced_patterns
        
        return contextual_patterns
    
    def generate_training_data(self):
        intents = []
        
        # Generate contextual patterns first
        contextual_patterns = self.generate_contextual_patterns()
        
        for tag, data in self.base_intents.items():
            # Get base patterns
            base_patterns = data["patterns"]
            
            # Add contextual patterns if available
            if tag in contextual_patterns:
                base_patterns.extend(contextual_patterns[tag])
            
            # Generate variations
            enhanced_patterns = self.generate_variations(base_patterns)
            
            # Remove duplicates and ensure uniqueness
            unique_patterns = list(set(enhanced_patterns))
            
            intents.append({
                "tag": tag,
                "patterns": unique_patterns,
                "responses": data["responses"]
            })
        
        return {"intents": intents}
    
    def save_to_file(self, filename="brain/data/intents.json"):
        data = self.generate_training_data()
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        total_patterns = sum(len(intent["patterns"]) for intent in data["intents"])
        print(f"✅ Generated training data with:")
        print(f"   • {len(data['intents'])} intents")
        print(f"   • {total_patterns} total patterns")
        
        # Print summary
        print("\n📊 Intent Summary:")
        for intent in data["intents"]:
            print(f"   • {intent['tag']}: {len(intent['patterns'])} patterns")
    
    def generate_vocabulary(self):
        """Generate vocabulary from all patterns"""
        all_patterns = []
        for intent in self.generate_training_data()["intents"]:
            all_patterns.extend(intent["patterns"])
        
        # Extract all unique words
        all_words = set()
        for pattern in all_patterns:
            words = pattern.lower().split()
            all_words.update(words)
        
        # Create vocabulary mapping
        vocabulary = {word: idx for idx, word in enumerate(sorted(all_words))}
        
        # Save vocabulary
        vocab_path = Path("brain/data/vocab.json")
        with open(vocab_path, 'w') as f:
            json.dump(vocabulary, f, indent=2)
        
        print(f"✅ Generated vocabulary with {len(vocabulary)} words")
        return vocabulary

# Standalone function to generate data
def generate_training_data():
    """Generate training data and vocabulary"""
    print("🧠 Generating training data for Aetherium AI...")
    
    generator = TrainingDataGenerator()
    generator.save_to_file()
    generator.generate_vocabulary()
    
    print("🎉 Training data generation complete!")

if __name__ == "__main__":
    generate_training_data()