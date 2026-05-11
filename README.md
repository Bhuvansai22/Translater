# English to Kannada Translator

A browser-based Python application to translate English text to Kannada using Google Translate.

## Features

- **Text Translation**: Translate text directly in the browser
- **File Translation**: Upload a text file and download the translated output
- **Web Interface**: Clean, responsive website with copy-to-clipboard support
- **Reusable Translator Core**: Translation logic stays in `translator.py`

## Installation

1. **Install Python** (3.7 or higher)

2. **Navigate to the project directory**:
   ```bash
   cd e:\Projects\Tanslater
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Website

Run the web app:
```bash
python main.py
```

Then open the site at:
```bash
http://127.0.0.1:5000
```

Website features:
- **Text Input Area**: Paste English text and translate it on the page
- **File Upload**: Upload a UTF-8 `.txt` file and download the Kannada translation
- **Copy Button**: Copy the translated text from the result area

### Programmatic Usage

```python
from translator import EnglishToKannadaTranslator

# Create translator instance
translator = EnglishToKannadaTranslator()

# Translate text
english_text = "Hello, how are you?"
kannada_text = translator.translate(english_text)
print(kannada_text)  # Output: ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?

# Translate file
translator.translate_file("input.txt", "output.txt")
```

## Project Structure

```
Tanslater/
├── requirements.txt      # Python dependencies
├── translator.py         # Core translation module
├── main.py               # Flask web application entry point
├── gui.py                # Legacy Tkinter interface
├── templates/            # HTML templates
├── static/                # CSS and frontend assets
└── README.md            # This file
```

## Dependencies

- **deep-translator** (1.11.4) - Google Translate API wrapper
- **Flask** (3.0.3) - Web framework

## How It Works

The translator uses the `googletrans` library, which:
- Wraps the Google Translate API
- Supports translation between multiple languages
- Requires internet connection for translation
- Automatically detects and handles language encoding

## Requirements

- Python 3.7+
- Internet connection (for translation service)
- Windows/Mac/Linux

## Example

**Input (English):**
```
Hello! How are you today? I hope you are doing well.
```

**Output (Kannada):**
```
ಹಲೋ! ಈ ದಿನ ನೀವು ಹೇಗಿದ್ದೀರಿ? ನೀವು ಚೆನ್ನಾಗಿ ಮಾಡುತ್ತಿದ್ದೀರಿ ಎಂದು ನಾನು ಆಶಿಸುತ್ತೇನೆ.
```

## Troubleshooting

- **Connection Error**: Ensure you have a stable internet connection
- **Module Not Found**: Run `pip install -r requirements.txt` again
- **Encoding Issues**: Ensure your text file is saved as UTF-8

## License

Open source project - feel free to modify and use as needed.

## Notes

- Translation quality depends on Google Translate's accuracy
- Special characters and formatting are preserved during translation
- File translations maintain the original line breaks and formatting
