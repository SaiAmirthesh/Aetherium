"""
Aetherium Brain Module - Contains the AI neural network and training logic.
"""

from .model import NeuralNetwork, AetheriumBrain
from .trainer import ModelTrainer

# Optional: You can define package-level variables or functions here
VERSION = "1.0.0"
AUTHOR = "Aetherium CLI"

# This makes the classes available when importing the package
# Now you can do: from brain import AetheriumBrain, ModelTrainer