import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from PIL import Image
import io

class Model:
    def __init__(self) -> None:
        genai.configure(api_key="AIzaSyCOeQQMrsEc6mB1GQK3lJHV85dAd7U3Who")
        self.model_text = genai.GenerativeModel("gemini-pro")
        self.model_image = genai.GenerativeModel("gemini-pro-vision")
        self.current_chat = []
        self.text_models = {}
        self.chat_text = self.model_text.start_chat(history=self.current_chat)
        self.safety_settings ={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
        }
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
    def text_model(self, text_model_id, message="Hello?"):
        response = self.text_models[text_model_id].send_message(message, stream=True)
        #response = self.get_chat(user).send_message(message, stream=True)
        return response
    
    def image_model(self, image_model_id, img, message = None):
        img_bytes = img.read()
        pil_image = Image.open(io.BytesIO(img_bytes))
        if message == None:
            response = self.model_image.generate_content(pil_image, stream=True, safety_settings=self.safety_settings)
        else:
            response = self.model_image.generate_content([message,pil_image], stream=True, safety_settings=self.safety_settings)
        
        return response
        
    
    def set_chat(self, text_model_id, current_chat = [], overide=False):
        if text_model_id not in self.text_models or overide:
            print(current_chat)
            self.text_models[text_model_id] = self.model_text.start_chat(history=current_chat)
        return self.text_models[text_model_id]

    def get_chat_model(self, text_model_id):
        return self.text_models[text_model_id]