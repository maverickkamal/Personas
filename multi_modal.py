import streamlit as st
from io import BytesIO
from llama_index.multi_modal_llms.gemini import GeminiMultiModal

model = genai.GenerativeModel('gemini-pro')


class ImageDocument:
    def __init__(self, image_data):
        self.image_data = image_data

    def resolve_image(self):
        return BytesIO(self.image_data)

class ImageProcessor:
    def __init__(self, gemini_pro):
        self.gemini_pro = gemini_pro

    def process_images(self, file_paths):
        image_documents = [self._read_image(file_path) for file_path in file_paths]
        return image_documents

    def _read_image(self, file_path):
        with open(file_path, "rb") as file:
            image_data = file.read()
        return ImageDocument(image_data)

    def gemini(self, prompt, file_paths):
        image_documents = self.process_images(file_paths)
        stream_complete_response = self.gemini_pro.stream_complete(
            prompt=prompt,
            image_documents=image_documents,
        )

        for r in stream_complete_response:
            print(r.text, end="")



def gemini_wrapper(prompt):
    image_processor = ImageProcessor(gemini_pro)
    file_paths = image_processor.get_file_paths()
    image_processor.gemini(prompt, file_paths)
