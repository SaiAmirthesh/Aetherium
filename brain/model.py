import numpy as np
import json
import os
from pathlib import Path

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.weights1 = np.random.randn(input_size, hidden_size)
        self.weights2 = np.random.randn(hidden_size, output_size)
        self.bias1 = np.zeros((1, hidden_size))
        self.bias2 = np.zeros((1, output_size))
        
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def forward(self, X):
        self.hidden = self.sigmoid(np.dot(X, self.weights1) + self.bias1)
        output = self.sigmoid(np.dot(self.hidden, self.weights2) + self.bias2)
        return output
    
    def predict(self, X):
        return self.forward(X)

class AetheriumBrain:
    def __init__(self):
        self.model = None
        self.vocab = {}
        self.intents = []
        self.model_path = Path("brain/models/aetherium_model.npy")
        self.vocab_path = Path("brain/data/vocab.json")
        self.intents_path = Path("brain/data/intents.json")
        self.windows_data_path = Path("brain/data/combined_windows_commands.json")
        
        self.load_or_initialize()
    
    def load_or_initialize(self):
        """Load Windows command data if available, otherwise initialize with basic data"""
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        self.vocab_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Priority 1: Load Windows command data if available
        if self.windows_data_path.exists():
            try:
                with open(self.windows_data_path, 'r') as f:
                    windows_data = json.load(f)
                self.intents = windows_data["intents"]
                print("✅ Loaded Windows command training data")
                # Generate vocabulary from Windows data
                self.generate_vocabulary_from_intents()
                self.save_data()
                return
            except Exception as e:
                print(f"❌ Error loading Windows data: {e}")
        
        # Priority 2: Load existing model if available
        if self.model_path.exists():
            self.load_model()
        else:
            # Priority 3: Initialize with basic data
            self.initialize_model()
    
    def generate_vocabulary_from_intents(self):
        """Generate vocabulary from the loaded intents"""
        all_words = set()
        
        for intent in self.intents:
            for pattern in intent["patterns"]:
                words = pattern.lower().split()
                all_words.update(words)
        
        # Create vocabulary mapping
        self.vocab = {word: idx for idx, word in enumerate(sorted(all_words))}
        
        # Save vocabulary
        with open(self.vocab_path, 'w') as f:
            json.dump(self.vocab, f, indent=2)
        
        print(f"✅ Generated vocabulary with {len(self.vocab)} words from Windows data")
    
    def initialize_model(self):
        """Initialize with basic Windows command vocabulary"""
        print("⚠️  Initializing with basic Windows command data...")
        
        # Basic Windows command vocabulary
        self.vocab = {
            # File operations
            'dir': 0, 'ls': 0, 'list': 0, 'files': 0, 'show': 0,
            'copy': 1, 'cp': 1, 'move': 1, 'mv': 1, 'rename': 1, 'ren': 1,
            'del': 2, 'delete': 2, 'rm': 2, 'remove': 2, 'erase': 2,
            'mkdir': 3, 'md': 3, 'create': 3, 'make': 3, 'new': 3,
            
            # System commands
            'systeminfo': 4, 'system': 4, 'info': 4, 'information': 4,
            'tasklist': 5, 'task': 5, 'process': 5, 'processes': 5,
            'ipconfig': 6, 'ip': 6, 'network': 6, 'config': 6,
            'ping': 7, 'net': 7, 'connection': 7,
            
            # Common words
            'how': 8, 'to': 8, 'use': 8, 'run': 8, 'execute': 8,
            'what': 9, 'does': 9, 'do': 9, 'explain': 9,
            'windows': 10, 'cmd': 10, 'command': 10, 'prompt': 10,
            
            # File types and objects
            'file': 11, 'files': 11, 'document': 11, 'folder': 11,
            'text': 12, 'txt': 12, 'python': 12, 'py': 12,
            
            # Help and greetings
            'help': 13, 'please': 13, 'assist': 13, 'support': 13,
            'hello': 14, 'hi': 14, 'hey': 14, 'greetings': 14
        }
        
        # Basic Windows command intents
        self.intents = [
            {
                "tag": "file_management",
                "patterns": [
                    "list files", "show files", "dir", "ls", "display files",
                    "copy file", "move file", "rename file", "delete file",
                    "create folder", "make directory", "remove file"
                ],
                "responses": ["Performing file operation..."]
            },
            {
                "tag": "system_info", 
                "patterns": [
                    "system information", "system info", "system status",
                    "computer info", "show system", "windows info"
                ],
                "responses": ["Gathering system information..."]
            },
            {
                "tag": "network_commands",
                "patterns": [
                    "ip config", "network configuration", "ipconfig",
                    "ping address", "test connection", "network status"
                ],
                "responses": ["Executing network command..."]
            },
            {
                "tag": "process_management",
                "patterns": [
                    "task list", "running processes", "show tasks",
                    "process list", "taskkill", "end process"
                ],
                "responses": ["Managing processes..."]
            },
            {
                "tag": "greeting",
                "patterns": ["hello", "hi", "hey", "greetings", "howdy"],
                "responses": ["Hello! How can I help with Windows commands?"]
            }
        ]
        
        self.save_data()
        print("✅ Initialized with basic Windows command data")
    
    def text_to_vector(self, text):
        """Convert text to numerical vector using current vocabulary"""
        words = text.lower().split()
        vector = np.zeros(len(self.vocab))
        
        for word in words:
            if word in self.vocab:
                vector[self.vocab[word]] += 1
        
        return vector
    
    def predict_intent(self, text):
        """Predict the intent of user input with Windows command focus"""
        vector = self.text_to_vector(text)
        
        # If model is trained, use it
        if self.model:
            prediction = self.model.predict(vector.reshape(1, -1))
            if np.max(prediction) > 0.3:  # Lower threshold for better matching
                intent_idx = np.argmax(prediction)
                return {
                    "tag": self.intents[intent_idx]["tag"], 
                    "response": np.random.choice(self.intents[intent_idx]["responses"])
                }
        
        # Fallback to rule-based matching for Windows commands
        return self.windows_rule_based_fallback(text)
    
    def windows_rule_based_fallback(self, text):
        """Rule-based intent matching optimized for Windows commands"""
        text_lower = text.lower()
        
        # Windows command specific matching
        if any(word in text_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return {"tag": "greeting", "response": "Hello! I can help with Windows commands."}
        
        elif any(word in text_lower for word in ['list', 'show', 'display', 'dir', 'ls', 'files']):
            return {"tag": "list_files", "response": "I'll list the files for you."}
        
        elif any(word in text_lower for word in ['create', 'make', 'new', 'touch', 'write']):
            return {"tag": "create_file", "response": "I can help create a file or folder."}
        
        elif any(word in text_lower for word in ['read', 'open', 'view', 'cat', 'type', 'show content']):
            return {"tag": "read_file", "response": "I'll read the file contents."}
        
        elif any(word in text_lower for word in ['delete', 'remove', 'rm', 'del', 'erase']):
            return {"tag": "delete_file", "response": "I can help delete files."}
        
        elif any(word in text_lower for word in ['system', 'info', 'status', 'health', 'specs', 'computer']):
            return {"tag": "system_info", "response": "Here's system information."}
        
        elif any(word in text_lower for word in ['process', 'task', 'running', 'programs', 'tasklist']):
            return {"tag": "process_list", "response": "Showing running processes."}
        
        elif any(word in text_lower for word in ['network', 'ip', 'connection', 'internet', 'ping', 'ipconfig']):
            return {"tag": "network_info", "response": "Executing network command."}
        
        elif any(word in text_lower for word in ['disk', 'storage', 'space', 'usage', 'capacity', 'df']):
            return {"tag": "disk_usage", "response": "Checking disk usage."}
        
        # ADD THESE NEW INTENTS FOR ADVANCED COMMANDS:
        elif any(word in text_lower for word in ['uptime', 'boot time', 'system uptime', 'how long running']):
            return {"tag": "system_uptime", "response": "Checking system uptime..."}
        
        elif any(word in text_lower for word in ['users', 'logged in', 'who is online', 'current users']):
            return {"tag": "users_online", "response": "Showing logged in users..."}
        
        elif any(word in text_lower for word in ['environment', 'env', 'variables', 'path', 'home']):
            return {"tag": "environment_vars", "response": "Showing environment variables..."}
        
        elif any(word in text_lower for word in ['services', 'running services', 'windows services', 'service status']):
            return {"tag": "running_services", "response": "Checking running services..."}
        
        elif any(word in text_lower for word in ['run', 'execute', 'command', 'cmd', 'windows']):
            # Extract the actual command to run
            words = text_lower.split()
            potential_commands = [word for word in words if word in [
                'dir', 'copy', 'move', 'del', 'mkdir', 'systeminfo', 'tasklist', 
                'ipconfig', 'ping', 'netstat', 'chkdsk', 'format', 'uptime'
            ]]
            
            if potential_commands:
                return {"tag": "command_execution", "response": f"Executing {potential_commands[0]} command..."}
            else:
                return {"tag": "command_execution", "response": "I'll execute that command."}
        
        elif any(word in text_lower for word in ['help', 'assist', 'support', 'how to']):
            return {"tag": "help", "response": "I can help with Windows commands like dir, copy, systeminfo, tasklist, ipconfig, uptime, etc."}
        
        else:
            return {"tag": "unknown", "response": "I'm not sure about that Windows command. Try: dir, copy, systeminfo, tasklist, ipconfig, uptime"}
    
    
    def save_data(self):
        """Save model and data"""
        # Save model weights if model exists
        if self.model:
            np.save(self.model_path, {
                'weights1': self.model.weights1,
                'weights2': self.model.weights2,
                'bias1': self.model.bias1,
                'bias2': self.model.bias2
            })
        
        # Save vocabulary
        with open(self.vocab_path, 'w') as f:
            json.dump(self.vocab, f, indent=2)
        
        # Save intents
        with open(self.intents_path, 'w') as f:
            json.dump({"intents": self.intents}, f, indent=2)
    
    def load_model(self):
        """Load saved model and data"""
        try:
            # Load model weights
            data = np.load(self.model_path, allow_pickle=True).item()
            self.model = NeuralNetwork(len(self.vocab), 8, len(self.intents))
            self.model.weights1 = data['weights1']
            self.model.weights2 = data['weights2']
            self.model.bias1 = data['bias1']
            self.model.bias2 = data['bias2']
            
            # Load vocabulary
            with open(self.vocab_path, 'r') as f:
                self.vocab = json.load(f)
            
            # Load intents
            with open(self.intents_path, 'r') as f:
                self.intents = json.load(f)["intents"]
                
            print("✅ Loaded trained model and data")
                
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("⚠️  Falling back to rule-based system")
            self.initialize_model()

    def get_available_commands(self):
        """Return list of available Windows commands for help"""
        commands = set()
        for intent in self.intents:
            if "file_management" in intent["tag"]:
                commands.update(["dir", "copy", "move", "del", "mkdir", "rmdir"])
            elif "system_info" in intent["tag"]:
                commands.update(["systeminfo", "tasklist", "whoami"])
            elif "network_commands" in intent["tag"]:
                commands.update(["ipconfig", "ping", "netstat"])
        
        return sorted(commands)