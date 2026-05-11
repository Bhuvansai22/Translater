"""English to Kannada Translator - Web Application."""

from io import BytesIO

from flask import Flask, render_template, request, send_file

from translator import EnglishToKannadaTranslator


app = Flask(__name__)
translator = EnglishToKannadaTranslator()


@app.get("/")
def index():
    """Render the translation website."""

    return render_template("index.html", translation_text="", source_text="", error_message="")


@app.post("/translate")
def translate_text():
    """Translate text submitted from the web form."""

    source_text = request.form.get("source_text", "").strip()

    if not source_text:
        return render_template(
            "index.html",
            translation_text="",
            source_text="",
            error_message="Please enter English text to translate.",
        )

    translated_text = translator.translate(source_text)

    return render_template(
        "index.html",
        translation_text=translated_text,
        source_text=source_text,
        error_message="",
    )


@app.post("/translate-file")
def translate_file():
    """Translate an uploaded text file and return the Kannada output as a download."""

    upload = request.files.get("input_file")

    if not upload or not upload.filename:
        return render_template(
            "index.html",
            translation_text="",
            source_text="",
            error_message="Please choose a text file to translate.",
        )

    try:
        source_text = upload.read().decode("utf-8")
    except UnicodeDecodeError:
        return render_template(
            "index.html",
            translation_text="",
            source_text="",
            error_message="The uploaded file must be UTF-8 encoded.",
        )

    translated_text = translator.translate(source_text)
    output = BytesIO(translated_text.encode("utf-8"))
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="kannada_translation.txt",
        mimetype="text/plain; charset=utf-8",
    )


def main():
    """Run the web app."""

    app.run(debug=True)


if __name__ == "__main__":
    main()