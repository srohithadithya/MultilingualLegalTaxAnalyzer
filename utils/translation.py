from googletrans import Translator

translator = Translator()

def translate_text(text, src_language='auto', dest_language='en'):
    """
    Translates text using Google Translate API.
    """
    translated = translator.translate(text, src=src_language, dest=dest_language)
    return translated.text