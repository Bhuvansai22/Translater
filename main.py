"""English to Kannada Translator - Web Application."""

from io import BytesIO
import json

from flask import Flask, render_template, request, send_file, jsonify

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


def main():
    """Run the web app."""

    app.run(debug=True)


if __name__ == "__main__":
    main()