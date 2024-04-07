import google.generativeai as genai
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
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
    def text_model(self, request, message="Hello?"):
        user = request.user
        response = self.text_models[user.username].send_message(message, stream=True)
        #response = self.get_chat(user).send_message(message, stream=True)
        return response
    
    def image_model(self, request, img, message = None):
        user = request.user
        img_bytes = img.read()
        pil_image = Image.open(io.BytesIO(img_bytes))
        if message == None:
            response = self.model_image.generate_content(pil_image, stream=True)
        else:
            response = self.model_image.generate_content([message,pil_image], stream=True)
        
        return response
        
    
    def set_chat(self, user):
        self.text_models[user.username] = self.model_text.start_chat(history=self.current_chat)
        return self.text_models[user.username]
