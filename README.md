# ⚡ Aetherium AI Assistant

![Aetherium](https://img.shields.io/badge/Aetherium-AI%2520Assistant-purple)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8%252B-green)
![License](https://img.shields.io/badge/License-MIT-orange)

A powerful, self-contained AI-powered command-line and graphical assistant built with custom neural networks.  
Aetherium combines the power of machine learning with practical system utilities in a beautiful purple-and-black themed interface.

---

## 📑 Table of Contents
- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [📋 Usage Examples](#-usage-examples)
- [🏗️ Project Structure](#️-project-structure)
- [🧠 AI Architecture](#-ai-architecture)
- [🎨 GUI Features](#-gui-features)
- [⚙️ Configuration](#️-configuration)
- [🔧 Advanced Usage](#-advanced-usage)
- [🐛 Troubleshooting](#-troubleshooting)
- [📈 Performance Metrics](#-performance-metrics)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)
- [🏆 Acknowledgments](#-acknowledgments)
- [📞 Support](#-support)
- [🔮 Future Roadmap](#-future-roadmap)

---

## ✨ Features

### 🤖 AI-Powered Intelligence
- **Custom Neural Network** – Built-from-scratch AI model  
- **Natural Language Processing** – Understands conversational commands  
- **13+ Intent Categories** – File operations, system commands, coding assistance  
- **Continuous Learning** – Improves with user interactions  

### 🖥️ Dual Interface
- **CLI Mode** – Full terminal integration with Typer  
- **GUI Mode** – Beautiful graphical interface with purple theme  
- **Quick Actions** – One-click common commands  

### 🔧 System Integration
- **File Operations** – Create, read, delete, list files  
- **System Monitoring** – Process list, disk usage, network info  
- **Command Execution** – Run system commands safely  
- **Real-time Feedback** – Instant command execution and results  

### 🎨 Beautiful Design
- **Aetherium Theme** – Stunning purple and black color scheme  
- **Modern GUI** – Intuitive and user-friendly interface  
- **Responsive Design** – Works flawlessly on different screen sizes  

### 🏗️ Project Structure

```graphql
Aetherium/
├── main.py                 # Main CLI entry point
├── gui.py                  # Graphical user interface
├── brain/                  # AI core components
│   ├── __init__.py
│   ├── model.py            # Neural network implementation
│   ├── trainer.py          # Model training logic
│   ├── data_generator.py   # Training data generation
│   └── data/               # Training data and vocabulary
├── commands/               # Command handlers
│   ├── __init__.py
│   ├── system.py           # System monitoring commands
│   └── file_ops.py         # File operations
├── config.py               # Application configuration
├── setup.py                # Installation script
├── requirements.txt        # Dependencies
└── README.md               # This file
```

### 🧠 AI Architecture

      Neural Network Design
      Input Layer: 50 neurons (vocabulary size)
      Hidden Layer: 8 neurons with sigmoid activation
      Output Layer: 13 neurons (intent categories)
      Learning Rate: 0.1
      Activation: Sigmoid function

### Training Data

      847+ training patterns across 13 intents
      234-word vocabulary with comprehensive coverage
      Automatic data generation with variations

### Supported Intents

      Greeting 👋
      List Files 📁
      Create File 📝
      Read File 👁️
      Delete File 🗑️
      System Info 🖥️
      Process List ⚡
      Disk Usage 💾
      Network Info 🌐
      Run Command 🚀
      Help ❓
      Python Code 🐍
      Git Operations 🔄

⭐ Star this repo if you find Aetherium useful!

💜 Built with passion for the open source community.

🚀 Experience the future of CLI and GUI interaction with Aetherium AI Assistant!
