import os
from flask import request, session, render_template, redirect, url_for
from utils.google_vision_ocr import extract_text_with_google_vision
from utils.translation import translate_text
from utils.nlp import analyze_and_structure_parsed_data
from utils.tts import text_to_speech

def setup_routes(app):
    @app.route('/dashboard')
    def dashboard():
        if "username" not in session:
            return redirect(url_for('login_page'))
        return render_template('dashboard.html')

    @app.route('/upload', methods=['POST'])
    def upload_file():
        target_language = request.form['language']
        uploaded_file = request.files['file']

        if not uploaded_file:
            return render_template('dashboard.html', error="No file selected.")

        # Save the uploaded file locally
        file_path = os.path.join('example_inputs', uploaded_file.filename)
        uploaded_file.save(file_path)

        # Extract text using Google Vision
        extracted_text = extract_text_with_google_vision(file_path)

        # Translate text
        translated_text = translate_text(extracted_text, dest_language=target_language)

        # Split text into sentences for display and speech
        sentences = translated_text.split(". ")
        sentence_audio_paths = []

        # Generate speech for each sentence
        for idx, sentence in enumerate(sentences):
            if sentence.strip():
                audio_path = text_to_speech(sentence.strip(), language=target_language, filename=f"sentence_{idx}")
                sentence_audio_paths.append((sentence, audio_path))

        # Save translated text
        translated_text_path = os.path.join('output', f'translated_text_{target_language}.txt')
        with open(translated_text_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(sentences))

        # Analyze structured data
        structured_data = analyze_and_structure_parsed_data(translated_text)
        translated_structured_data = translate_text(
            format_structured_data(structured_data), 
            dest_language=target_language
        )

        # Save structured data
        structured_data_path = os.path.join('output', f'structured_data_{target_language}.txt')
        with open(structured_data_path, 'w', encoding='utf-8') as f:
            f.write(translated_structured_data)

        # Render the enhanced results page
        return render_template(
            'result.html',
            sentences=sentence_audio_paths,
            structured_data=translated_structured_data,
            translated_text_path=translated_text_path,
            structured_data_path=structured_data_path
        )

def format_structured_data(data):
    """
    Formats structured data for translation and saving.
    """
    return (
        f"Client Name: {data['Client Name']}\n"
        f"PAN: {data['PII Data']['PAN']}\n"
        f"GSTIN: {data['PII Data']['GSTIN']}\n"
        f"Nature of Notice: {data['Nature of Notice']}\n"
        f"Deadline: {data['Deadlines and Penalties']['Deadline']}\n"
        f"Penalty: {data['Deadlines and Penalties']['Penalty']}\n"
        f"Reporting Officer/Office: {data['Reporting Officer/Office']}\n"
        f"Relevant Legal Sections: {', '.join(data['Relevant Legal Sections'])}\n"
    )