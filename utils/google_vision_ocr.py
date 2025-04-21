from google.cloud import vision

def extract_text_with_google_vision(file_path):
    """
    Extracts text from images or PDFs using Google Cloud Vision API.
    """
    # Initialize Vision API client
    client = vision.ImageAnnotatorClient()

    with open(file_path, "rb") as file:
        content = file.read()
        image = vision.Image(content=content)

    # Perform text detection
    response = client.text_detection(image=image)
    if response.error.message:
        raise Exception(f"Google Vision API Error: {response.error.message}")

    # Return extracted text
    return response.full_text_annotation.text.strip()