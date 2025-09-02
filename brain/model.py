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
        
        self.load_or_initialize()
    
    def load_or_initialize(self):
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        self.vocab_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if data files exist, generate if not
        if not self.intents_path.exists() or not self.vocab_path.exists():
            self.generate_missing_data()
        
        if self.model_path.exists():
            self.load_model()
        else:
            self.initialize_model()

    def generate_missing_data(self):
        """Generate missing data files"""
        try:
            from brain.data_generator import TrainingDataGenerator
            generator = TrainingDataGenerator()
            if not self.intents_path.exists():
                generator.save_to_file(str(self.intents_path))
            if not self.vocab_path.exists():
                generator.generate_vocabulary()
        except ImportError:
            self.initialize_model()


    def initialize_model(self):
        self.vocab = {
            'hello': 0, 'hi': 0, 'hey': 0, 'greetings': 0,
            'list': 1, 'show': 1, 'display': 1, 'dir': 1, 'ls': 1,
            'create': 2, 'make': 2, 'new': 2, 'touch': 2,
            'delete': 3, 'remove': 3, 'rm': 3, 'del': 3,
            'file': 4, 'files': 4, 'directory': 4, 'folder': 4,
            'system': 5, 'process': 5, 'task': 5, 'info': 5,
            'run': 6, 'execute': 6, 'command': 6,
            'help': 7, 'assist': 7, 'support': 7,
            'python': 8, 'script': 8, 'code': 8,
            'git': 9, 'version': 9, 'clone': 9
        }
        
        self.intents = [
            {"tag": "greeting", "patterns": ["hello", "hi", "hey", "greetings"], "responses": ["Hello!", "Hi there!", "Hey! How can I help?"]},
            {"tag": "list_files", "patterns": ["list files", "show files", "display files", "dir", "ls"], "responses": ["Listing files..."]},
            {"tag": "create_file", "patterns": ["create file", "make file", "new file", "touch file"], "responses": ["Creating file..."]},
            {"tag": "delete_file", "patterns": ["delete file", "remove file", "rm file", "del file"], "responses": ["Deleting file..."]},
            {"tag": "system_info", "patterns": ["system info", "system status", "system health"], "responses": ["Showing system information..."]},
            {"tag": "run_command", "patterns": ["run command", "execute command", "run program"], "responses": ["Executing command..."]},
            {"tag": "help", "patterns": ["help", "assist", "support", "how to"], "responses": ["I'm here to help!"]},
            {"tag": "python", "patterns": ["python script", "run python", "execute code"], "responses": ["Running Python code..."]},
            {"tag": "git", "patterns": ["git command", "version control", "clone repo"], "responses": ["Git operations..."]}
        ]
        
        self.save_data()
    
    def text_to_vector(self, text):
        words = text.lower().split()
        vector = np.zeros(len(self.vocab))
        
        for word in words:
            if word in self.vocab:
                vector[self.vocab[word]] += 1
        
        return vector
    
    def predict_intent(self, text):
        vector = self.text_to_vector(text)
        
        if self.model:
            prediction = self.model.predict(vector.reshape(1, -1))
            if np.max(prediction) > 0.5:
                intent_idx = np.argmax(prediction)
                return {"tag": self.intents[intent_idx]["tag"], "response": np.random.choice(self.intents[intent_idx]["responses"])}
        
        return self.rule_based_fallback(text)
    
    def rule_based_fallback(self, text):
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return {"tag": "greeting", "response": "Hello! How can I help you today?"}
        elif any(word in text_lower for word in ['list', 'show', 'display', 'dir', 'ls']):
            return {"tag": "list_files", "response": "I'll list the files for you."}
        elif any(word in text_lower for word in ['create', 'make', 'new', 'touch']):
            return {"tag": "create_file", "response": "I can help create a file."}
        elif any(word in text_lower for word in ['delete', 'remove', 'rm', 'del']):
            return {"tag": "delete_file", "response": "I can help delete a file."}
        elif any(word in text_lower for word in ['system', 'info', 'status', 'health']):
            return {"tag": "system_info", "response": "Here's system information."}
        elif any(word in text_lower for word in ['run', 'execute', 'command']):
            return {"tag": "run_command", "response": "I'll execute that command."}
        elif any(word in text_lower for word in ['help', 'assist', 'support']):
            return {"tag": "help", "response": "I'm here to help! What do you need?"}
        elif any(word in text_lower for word in ['python', 'code', 'script']):
            return {"tag": "python", "response": "Python code execution."}
        elif any(word in text_lower for word in ['git', 'version', 'clone']):
            return {"tag": "git", "response": "Git operations."}
        else:
            return {"tag": "unknown", "response": "I'm not sure how to help with that. Try asking about files, system commands, or code execution."}
    
    def save_data(self):
        np.save(self.model_path, {
            'weights1': self.model.weights1 if self.model else np.random.randn(50, 8),
            'weights2': self.model.weights2 if self.model else np.random.randn(8, 10),
            'bias1': self.model.bias1 if self.model else np.zeros((1, 8)),
            'bias2': self.model.bias2 if self.model else np.zeros((1, 10))
        })
        
        with open(self.vocab_path, 'w') as f:
            json.dump(self.vocab, f)
        
        with open(self.intents_path, 'w') as f:
            json.dump(self.intents, f)
    
    def load_model(self):
        try:
            data = np.load(self.model_path, allow_pickle=True).item()
            self.model = NeuralNetwork(len(self.vocab), 8, len(self.intents))
            self.model.weights1 = data['weights1']
            self.model.weights2 = data['weights2']
            self.model.bias1 = data['bias1']
            self.model.bias2 = data['bias2']
            
            with open(self.vocab_path, 'r') as f:
                self.vocab = json.load(f)
            
            with open(self.intents_path, 'r') as f:
                self.intents = json.load(f)
                
        except Exception as e:
            print(f"Error loading model: {e}")
            self.initialize_model()