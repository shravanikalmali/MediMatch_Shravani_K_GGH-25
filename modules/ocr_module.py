import io
from google.cloud import vision

def detect_text(image_path):
    """
    Uses Google Cloud Vision API to extract text from the image.
    Returns:
      - full_text: The complete detected text.
      - word_boxes: A list of tuples (word, bounding_box) for individual words.
    """
    client = vision.ImageAnnotatorClient()
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if response.error.message:
        raise Exception(f'API error: {response.error.message}')
    if not texts:
        return "", []
    full_text = texts[0].description
    word_boxes = []
    for text in texts[1:]:
        vertices = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
        word_boxes.append((text.description, vertices))
    return full_text, word_boxes
