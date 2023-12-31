from llama_index.multi_modal_llms.gemini import GeminiMultiModal
import os
from dotenv import load_dotenv
#from typing import Sequence
from io import BytesIO


safety_settings=[
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_ONLY_HIGH",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_ONLY_HIGH",
    },
]
gemini_pro = GeminiMultiModal(model_name="models/gemini-pro-vision")
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
    # Use a list to store parts of the response
    
    response_parts = []
    
    for r in stream_complete_response:
        response_parts.append(r.text)

    # Concatenate all parts into a single string
    complete_response = "".join(response_parts)
    
    return complete_response

