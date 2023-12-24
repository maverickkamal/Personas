from llama_index.multi_modal_llms.gemini import GeminiMultiModal
import os
from dotenv import load_dotenv
#from typing import Sequence
from io import BytesIO

class ImageDocument:
    def __init__(self, image_data):
        self.image_data = image_data

    def resolve_image(self):
        return BytesIO(self.image_data)


def gemini(prompt, image_data):
    images_document = ImageDocument(image_data)
    stream_complete_response = gemini_pro.stream_complete(
        prompt=prompt,
        image_documents=[images_document],
    )
    response = stream_complete_response.text
    return response
