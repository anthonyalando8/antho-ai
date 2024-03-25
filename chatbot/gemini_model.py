import google.generativeai as genai
from PIL import Image
import io

class Model:
    def __init__(self) -> None:
        genai.configure(api_key="AIzaSyCOeQQMrsEc6mB1GQK3lJHV85dAd7U3Who")
        self.model_text = genai.GenerativeModel("gemini-pro")
        self.model_image = genai.GenerativeModel("gemini-pro-vision")
        self.current_chat = []
        self.chat_text = self.model_text.start_chat(history=self.current_chat)
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)

    def text_model(self, message="Hello?"):
        response = self.chat_text.send_message(message)
        print(self.chat_text.history)
        self.current_chat.extend(self.chat_text.history[-2:])
        print(self.current_chat)
        return self.current_chat
    
    def image_model(self, img, message = None,):
        chat_image = self.model_image.start_chat(history=[])
        img_bytes = img.read()
        pil_image = Image.open(io.BytesIO(img_bytes))
        if message == None:
            response = chat_image.send_message(pil_image)
        else:
            response = chat_image.send_message([message,pil_image])
            #response.resolve()
        
        self.current_chat.extend(chat_image.history[-2:])

        return self.current_chat
    
    def get_chats(self):
        return self.current_chat
