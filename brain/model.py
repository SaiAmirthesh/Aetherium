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
        """Load existing model or create new one"""
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        self.vocab_path.parent.mkdir(parents=True, exist_ok=True)
        
        if self.model_path.exists():
            self.load_model()
        else:
            self.initialize_model()
    
    def initialize_model(self):
        """Initialize with basic vocabulary and intents"""
        self.vocab = {
            'hello': 0, 'hi': 0, 'hey': 0,
            'list': 1, 'show': 1, 'display': 1,
            'create': 2, 'make': 2, 'new': 2,
            'delete': 3, 'remove': 3, 'rm': 3,
            'file': 4, 'files': 4, 'directory': 4,
            'system': 5, 'process': 5, 'task': 5
        }
        
        self.intents = [
            {"tag": "greeting", "patterns": ["hello", "hi", "hey"], "responses": ["Hello!", "Hi there!", "Hey!"]},
            {"tag": "list_files", "patterns": ["list files", "show files", "display files"], "responses": ["Listing files..."]},
            {"tag": "create_file", "patterns": ["create file", "make file", "new file"], "responses": ["Creating file..."]},
            {"tag": "system_info", "patterns": ["system info", "system status", "task list"], "responses": ["Showing system information..."]}
        ]
        
        self.save_data()
    
    def text_to_vector(self, text):
        """Convert text to numerical vector"""
        words = text.lower().split()
        vector = np.zeros(len(self.vocab))
        
        for word in words:
            if word in self.vocab:
                vector[self.vocab[word]] += 1
        
        return vector
    
    def predict_intent(self, text):
        """Predict the intent of user input"""
        vector = self.text_to_vector(text)
        prediction = self.model.predict(vector.reshape(1, -1))
        
        # Simple rule-based fallback
        if np.max(prediction) < 0.5:
            return self.rule_based_fallback(text)
        
        intent_idx = np.argmax(prediction)
        return self.intents[intent_idx]
    
    def rule_based_fallback(self, text):
        """Rule-based intent matching"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['hello', 'hi', 'hey']):
            return {"tag": "greeting", "response": "Hello! How can I help you?"}
        elif any(word in text_lower for word in ['list', 'show', 'dir', 'ls']):
            return {"tag": "list_files", "response": "I'll list the files for you."}
        elif any(word in text_lower for word in ['create', 'make', 'new', 'touch']):
            return {"tag": "create_file", "response": "I can help create a file."}
        elif any(word in text_lower for word in ['system', 'task', 'process', 'info']):
            return {"tag": "system_info", "response": "Here's system information."}
        else:
            return {"tag": "unknown", "response": "I'm not sure how to help with that. Try asking about files or system commands."}
    
    def save_data(self):
        """Save model and data"""
        np.save(self.model_path, {
            'weights1': self.model.weights1,
            'weights2': self.model.weights2,
            'bias1': self.model.bias1,
            'bias2': self.model.bias2
        })
        
        with open(self.vocab_path, 'w') as f:
            json.dump(self.vocab, f)
        
        with open(self.intents_path, 'w') as f:
            json.dump(self.intents, f)
    
    def load_model(self):
        """Load saved model"""
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