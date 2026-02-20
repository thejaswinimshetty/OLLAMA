# Ollama Desktop Chatbot

A modern, ChatGPT-like desktop chatbot application built with Python Tkinter and powered by Ollama.

## Features

- 🎨 Modern dark theme UI similar to ChatGPT
- 💬 Chat bubbles (user on right, bot on left)
- 📜 Scrollable chat history
- ⚡ Streaming responses (text appears gradually)
- 🧠 Conversation context memory
- 🎯 Clean and intuitive interface
- ⚠️ Proper error handling

## Prerequisites

1. **Python 3.7+** installed on your system
2. **Ollama** installed and running

### Install Ollama

Visit [https://ollama.ai](https://ollama.ai) and download Ollama for your operating system.

After installation, pull the llama3 model:

```bash
ollama pull llama3
```

## Installation

1. Clone or download this repository

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Start Ollama Server

Make sure Ollama is running. Open a terminal and run:

```bash
ollama serve
```

Keep this terminal open while using the chatbot.

### Step 2: Run the Chatbot

In a new terminal, run:

```bash
python chatbot.py
```

### Step 3: Start Chatting!

- Type your message in the input field at the bottom
- Press Enter or click "Send" to send your message
- Use Shift+Enter for multiline messages
- Watch the bot's response stream in real-time

## Configuration

You can modify the chatbot settings in `chatbot.py`:

- **Model**: Change `self.model_name = "llama3"` to use a different Ollama model
- **API URL**: Change `self.ollama_url` if Ollama is running on a different port
- **Colors**: Modify the color variables in `__init__` for custom theming

## Available Ollama Models

To see available models:

```bash
ollama list
```

To pull a new model:

```bash
ollama pull <model-name>
```

Popular models:
- `llama3` - Meta's Llama 3 (recommended)
- `mistral` - Mistral 7B
- `codellama` - Code-specialized model
- `phi` - Microsoft's Phi model

## Troubleshooting

### "Cannot connect to Ollama" Error

- Make sure Ollama is running: `ollama serve`
- Check if Ollama is accessible: `curl http://localhost:11434`
- Verify the model is installed: `ollama list`

### Model Not Found

Pull the model first:

```bash
ollama pull llama3
```

### Slow Responses

- Larger models require more resources
- Try a smaller model like `phi` or `mistral`
- Ensure your system has adequate RAM

## Keyboard Shortcuts

- **Enter**: Send message
- **Shift+Enter**: New line in message
- **Ctrl+C**: Close application (in terminal)

## Technical Details

- **Frontend**: Python Tkinter
- **Backend**: Ollama API (REST)
- **Streaming**: Real-time response streaming
- **Threading**: Non-blocking UI with background API calls
- **Context**: Maintains conversation history

## License

MIT License - Feel free to modify and use as needed.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
