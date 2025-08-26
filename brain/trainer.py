import numpy as np
import json
from pathlib import Path
from .model import NeuralNetwork

class ModelTrainer:
    def __init__(self, brain):
        self.brain = brain
        self.training_data_path = Path("brain/data/training_data.json")
    
    def generate_training_data(self):
        """Generate training data from intents"""
        training_data = []
        
        for intent_idx, intent in enumerate(self.brain.intents):
            for pattern in intent['patterns']:
                # Convert pattern to vector
                vector = self.brain.text_to_vector(pattern)
                # Create target output (one-hot encoding)
                target = np.zeros(len(self.brain.intents))
                target[intent_idx] = 1
                
                training_data.append({
                    'input': vector.tolist(),
                    'target': target.tolist(),
                    'intent': intent['tag']
                })
        
        return training_data
    
    def train_model(self, epochs=1000, learning_rate=0.1):
        """Train the neural network"""
        print("🧠 Training AI model...")
        
        # Generate training data
        training_data = self.generate_training_data()
        
        if not training_data:
            print("❌ No training data available")
            return
        
        # Save training data
        self.training_data_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.training_data_path, 'w') as f:
            json.dump(training_data, f, indent=2)
        
        # Initialize model
        input_size = len(self.brain.vocab)
        output_size = len(self.brain.intents)
        self.brain.model = NeuralNetwork(input_size, 8, output_size)
        
        # Convert to numpy arrays
        X = np.array([data['input'] for data in training_data])
        y = np.array([data['target'] for data in training_data])
        
        # Training loop
        for epoch in range(epochs):
            # Forward pass
            hidden = self.brain.model.sigmoid(np.dot(X, self.brain.model.weights1) + self.brain.model.bias1)
            output = self.brain.model.sigmoid(np.dot(hidden, self.brain.model.weights2) + self.brain.model.bias2)
            
            # Backpropagation
            error = y - output
            delta_output = error * output * (1 - output)
            
            error_hidden = delta_output.dot(self.brain.model.weights2.T)
            delta_hidden = error_hidden * hidden * (1 - hidden)
            
            # Update weights and biases
            self.brain.model.weights2 += hidden.T.dot(delta_output) * learning_rate
            self.brain.model.bias2 += np.sum(delta_output, axis=0, keepdims=True) * learning_rate
            self.brain.model.weights1 += X.T.dot(delta_hidden) * learning_rate
            self.brain.model.bias1 += np.sum(delta_hidden, axis=0, keepdims=True) * learning_rate
            
            if epoch % 100 == 0:
                loss = np.mean(np.square(error))
                print(f"Epoch {epoch}, Loss: {loss:.4f}")
        
        print("✅ Training complete!")
        self.brain.save_data()
    
    def load_training_data(self):
        """Load training data from file"""
        if self.training_data_path.exists():
            with open(self.training_data_path, 'r') as f:
                return json.load(f)
        return []