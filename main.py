"""English to Kannada Translator - Web Application."""

from io import BytesIO
import json

from flask import Flask, render_template, request, send_file, jsonify
import asyncio
import edge_tts

from translator import MultiLanguageTranslator


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Properly encode unicode characters
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False# Default translator - will be changed based on user selection
default_translator = MultiLanguageTranslator('kannada')

# Language code mapping for filenames
LANGUAGE_FILENAMES = {
    'kannada': 'kannada_translation',
    'telugu': 'telugu_translation',
    'tamil': 'tamil_translation',
    'hindi': 'hindi_translation',
    'malayalam': 'malayalam_translation',
}

@app.get("/")
def index():
    """Render the translation website."""
    return render_template("index.html", translation_text="", source_text="", error_message="")


@app.post("/translate")
def translate_text():
    """Translate text submitted from the web form."""
    source_text = request.form.get("source_text", "").strip()
    target_language = request.form.get("target_language", "kannada").lower()

    if not source_text:
        response = jsonify({
            "success": False,
            "error": "Please enter English text to translate."
        })
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response, 400

    try:
        translator = MultiLanguageTranslator(target_language)
        translated_text = translator.translate(source_text)
        response = jsonify({
            "success": True,
            "translation": translated_text,
            "language": target_language
        })
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    except ValueError as e:
        response = jsonify({
            "success": False,
            "error": str(e)
        })
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response, 400
    except Exception as e:
        response = jsonify({
            "success": False,
            "error": f"Translation error: {str(e)}"
        })
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response, 500


@app.post("/translate-file")
def translate_file():
    """Translate an uploaded text file and return the translated output as a download."""
    upload = request.files.get("input_file")
    target_language = request.form.get("target_language", "kannada").lower()

    if not upload or not upload.filename:
        return render_template(
            "index.html",
            translation_text="",
            source_text="",
            error_message="Please choose a text file to translate.",
            target_language=target_language,
        )

    try:
        source_text = upload.read().decode("utf-8")
    except UnicodeDecodeError:
        return render_template(
            "index.html",
            translation_text="",
            source_text="",
            error_message="The uploaded file must be UTF-8 encoded.",
            target_language=target_language,
        )

    try:
        translator = MultiLanguageTranslator(target_language)
        translated_text = translator.translate(source_text)
    except ValueError as e:
        return render_template(
            "index.html",
            translation_text="",
            source_text="",
            error_message=str(e),
            target_language=target_language,
        )

    output = BytesIO(translated_text.encode("utf-8"))
    output.seek(0)
    
    # Generate filename based on language
    filename = LANGUAGE_FILENAMES.get(target_language, 'translation')

    return send_file(
        output,
        as_attachment=True,
        download_name=f"{filename}.txt",
        mimetype="text/plain; charset=utf-8",
    )


@app.post("/speak")
def speak():
    """Generate speech for the given text and language."""
    text = request.form.get("text", "").strip()
    lang = request.form.get("lang", "kannada").lower()
    gender = request.form.get("gender", "female").lower()
    
    # Map to edge-tts voices
    voice_map = {
        'kannada': {'female': 'kn-IN-SapnaNeural', 'male': 'kn-IN-GaganNeural'},
        'telugu': {'female': 'te-IN-ShrutiNeural', 'male': 'te-IN-MohanNeural'},
        'tamil': {'female': 'ta-IN-PallaviNeural', 'male': 'ta-IN-ValluvarNeural'},
        'hindi': {'female': 'hi-IN-SwaraNeural', 'male': 'hi-IN-MadhurNeural'},
        'malayalam': {'female': 'ml-IN-SobhanaNeural', 'male': 'ml-IN-MidhunNeural'}
    }
    
    lang_voices = voice_map.get(lang, voice_map['hindi'])
    voice = lang_voices.get(gender, lang_voices['female'])
    
    if not text:
        return jsonify({"success": False, "error": "No text provided"}), 400
        
    try:
        # Create an event loop to run the async edge-tts
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def generate_speech():
            communicate = edge_tts.Communicate(text, voice)
            data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    data += chunk["data"]
            return data

        audio_data = loop.run_until_complete(generate_speech())
        loop.close()
        
        fp = BytesIO(audio_data)
        return send_file(fp, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


def main():
    """Run the web app."""

    app.run(debug=True)


if __name__ == "__main__":
    main()