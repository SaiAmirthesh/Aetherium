# Aetherium

A Windows-native, AI-powered shell with a GUI.  
Uses Google Gemini API for natural language processing to convert user requests into Windows shell commands, executes them, and displays the output.

## Features

- **Natural Language Interface**: Type requests in plain English.
- **AI Powered**: Uses Gemini API (Google Generative AI).
- **Windows Shell Execution**: Runs commands and shows results.
- **Simple GUI**: Built with Tkinter.

## Getting Started

### Prerequisites

- Windows (recommended)
- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Google AI Studio](https://aistudio.google.com/) account (free API key)

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/SaiAmirthesh/Aetherium.git
   cd Aetherium
   ```

2. Create a virtual environment (optional but recommended):

   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Set your Gemini API key as an environment variable:

   - Get your API key from [Google AI Studio](https://aistudio.google.com).
   - Set it in your environment (Windows Command Prompt):

     ```sh
     set GEMINI_API_KEY=your-gemini-api-key
     ```

### Usage

```sh
python main.py
```

Type your requests in the GUI—e.g.  
`List all .txt files in my Documents folder.`

The AI will generate and run the Windows command for you.

## Configuration

Edit `ai_shell/config.py` to change the Gemini model or generation parameters.

## Notes

- Output depends on the Gemini model's instruction-following capabilities.
- For best results, use instruction-tuned models.

## Contributing

Pull requests are welcome!

## License

MIT