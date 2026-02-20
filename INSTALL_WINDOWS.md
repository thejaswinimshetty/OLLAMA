# Windows Installation Guide

## Quick Setup for Windows Users

### Step 1: Install Python Dependencies

Most dependencies install easily:

```bash
pip install requests PyPDF2 python-docx SpeechRecognition pyttsx3
```

### Step 2: Install PyAudio (Windows)

PyAudio can be tricky on Windows. Here are three methods:

#### Method 1: Using pip (Try this first)

```bash
pip install pyaudio
```

#### Method 2: Using Wheel File (If Method 1 fails)

1. Download the appropriate wheel file for your Python version from:
   https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

2. Choose based on your Python version:
   - Python 3.11: `PyAudio-0.2.11-cp311-cp311-win_amd64.whl`
   - Python 3.10: `PyAudio-0.2.11-cp310-cp310-win_amd64.whl`
   - Python 3.9: `PyAudio-0.2.11-cp39-cp39-win_amd64.whl`

3. Install the downloaded wheel:
   ```bash
   pip install PyAudio-0.2.11-cp311-cp311-win_amd64.whl
   ```

#### Method 3: Using pipwin

```bash
pip install pipwin
pipwin install pyaudio
```

### Step 3: Verify Installation

Test if everything works:

```bash
python -c "import pyaudio; print('PyAudio installed successfully!')"
```

### Step 4: Run the Chatbot

```bash
python chatbot.py
```

## Troubleshooting

### "Microsoft Visual C++ 14.0 is required"

Install Microsoft C++ Build Tools:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Microphone Not Working

1. Check Windows microphone permissions:
   - Settings → Privacy → Microphone
   - Allow apps to access microphone

2. Test microphone:
   ```bash
   python -m speech_recognition
   ```

### Voice Output Not Working

pyttsx3 should work out of the box on Windows. If issues occur:

```bash
pip uninstall pyttsx3
pip install pyttsx3==2.90
```

## Alternative: Run Without Voice Features

If you can't install PyAudio, you can modify the code to disable voice features:

1. Comment out voice-related imports in `chatbot.py`
2. Remove voice button functionality
3. The document upload and chat features will still work perfectly!

## Need Help?

- Check Python version: `python --version`
- Check pip version: `pip --version`
- Update pip: `python -m pip install --upgrade pip`
