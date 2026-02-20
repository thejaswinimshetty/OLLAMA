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
- 📄 **Document Upload** (PDF, TXT, DOCX) - Ask questions about your documents
- 🎤 **Voice Input** - Speak your questions
- 🔊 **Voice Output** - Listen to AI responses (Text-to-Speech)

## Prerequisites

1. **Python 3.7+** installed on your system
2. **Ollama** installed and running
3. **Microphone** (for voice input feature)

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

**Note for Windows users:** If you encounter issues installing PyAudio, download the appropriate wheel file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install it:

```bash
pip install PyAudio-0.2.11-cp3xx-cp3xx-win_amd64.whl
```

Replace `cp3xx` with your Python version (e.g., `cp311` for Python 3.11).

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
- Press Enter or click "Send ➤" to send your message
- Use Shift+Enter for multiline messages
- Watch the bot's response stream in real-time

### Step 4: Use Advanced Features

**Document Upload (📄):**
1. Click the 📄 button
2. Select a PDF, TXT, or DOCX file
3. Ask questions about the document content
4. Example: "Summarize this document" or "What are the key points?"

**Voice Input (🎤):**
1. Click the 🎤 button
2. Speak your question clearly
3. The text will appear in the input field
4. Click Send or press Enter

**Voice Output (🔊/🔇):**
1. Click 🔊 to enable voice responses
2. The AI will speak its answers
3. Click 🔇 to disable voice output

**Clear Chat (🗑️):**
- Click 🗑️ to clear conversation history and document context

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

### Voice Input Not Working

- Check microphone permissions
- Ensure microphone is connected and working
- Test with: `python -m speech_recognition`
- Requires internet for Google Speech Recognition

### Document Upload Issues

- Ensure file is not corrupted
- Check file permissions
- Large documents may take time to process
- PDF files must contain extractable text (not scanned images)

## Keyboard Shortcuts

- **Enter**: Send message
- **Shift+Enter**: New line in message
- **Ctrl+C**: Close application (in terminal)

## Supported Document Formats

- **PDF** (.pdf) - Portable Document Format
- **Text** (.txt) - Plain text files
- **Word** (.docx) - Microsoft Word documents

## Voice Features

**Voice Input:**
- Uses Google Speech Recognition
- Requires internet connection
- Supports multiple languages
- 10-second recording limit per input

**Voice Output:**
- Uses pyttsx3 (offline TTS)
- Works without internet
- Adjustable speed and volume
- Toggle on/off with 🔊/🔇 button

## Technical Details

- **Frontend**: Python Tkinter
- **Backend**: Ollama API (REST)
- **Streaming**: Real-time response streaming
- **Threading**: Non-blocking UI with background API calls
- **Context**: Maintains conversation history
- **Document Processing**: PyPDF2, python-docx
- **Voice Recognition**: SpeechRecognition (Google API)
- **Text-to-Speech**: pyttsx3 (offline)

## License

MIT License - Feel free to modify and use as needed.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
