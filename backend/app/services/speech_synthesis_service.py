# backend/app/services/speech_synthesis_service.py

# To use Google Cloud Text-to-Speech, uncomment the import and ensure GOOGLE_APPLICATION_CREDENTIALS is set
# from google.cloud import texttospeech_v1beta1 as texttospeech
from gtts import gTTS
import io
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Initialize Google Cloud Text-to-Speech client if credentials are set
# try:
#     if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
#         google_tts_client = texttospeech.TextToSpeechClient()
#         logger.info("Google Cloud Text-to-Speech client initialized.")
#     else:
#         google_tts_client = None
#         logger.warning("GOOGLE_APPLICATION_CREDENTIALS not set. Google Cloud Text-to-Speech will not be used.")
# except Exception as e:
#     google_tts_client = None
#     logger.error(f"Failed to initialize Google Cloud Text-to-Speech client: {e}")


def generate_speech_audio(text_to_speak, language='en'):
    """
    Generates an audio file (MP3) from text using gTTS (or Google Cloud Text-to-Speech if enabled).
    """
    if not text_to_speak:
        raise ValueError("Text to speak cannot be empty.")

    # Map language codes if necessary (e.g., Tesseract 'hin' to gTTS 'hi')
    gtts_lang_map = {
        'en': 'en', 'hi': 'hi', 'fr': 'fr', 'es': 'es', 'de': 'de', 'it': 'it',
        'pt': 'pt', 'ar': 'ar', 'zh-cn': 'zh-cn', 'ja': 'ja', 'ko': 'ko',
        'bn': 'bn', 'gu': 'gu', 'kn': 'kn', 'ml': 'ml', 'mr': 'mr', 'pa': 'pa',
        'ta': 'ta', 'te': 'te', # Indian languages might need specific support if gTTS/Google TTS doesn't cover
        'hin': 'hi' # Mapping Tesseract's 'hin' to gTTS's 'hi'
    }
    effective_lang_code = gtts_lang_map.get(language.lower(), 'en') # Default to English if not found

    try:
        # if google_tts_client:
        #     logger.info(f"Using Google Cloud TTS for: '{text_to_speak[:50]}...' to {effective_lang_code}")
        #     # Set the synthesis input
        #     synthesis_input = texttospeech.SynthesisInput(text=text_to_speak)
        #
        #     # Build the voice request, select the language code ("en-US") and the ssml
        #     # voice gender ("neutral")
        #     voice = texttospeech.VoiceSelectionParams(
        #         language_code=effective_lang_code,
        #         ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        #     )
        #
        #     # Select the type of audio file you want returned
        #     audio_config = texttospeech.AudioConfig(
        #         audio_encoding=texttospeech.AudioEncoding.MP3
        #     )
        #
        #     # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
        #     response = google_tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        #     return response.audio_content # The MP3 audio bytes
        # else:
        logger.info(f"Using gTTS for: '{text_to_speak[:50]}...' to {effective_lang_code}")
        tts = gTTS(text=text_to_speak, lang=effective_lang_code, slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer.getvalue()
    except Exception as e:
        logger.error(f"Failed to generate speech audio with gTTS/Google TTS for language {effective_lang_code}: {e}", exc_info=True)
        raise Exception(f"Failed to generate speech audio: {e}")