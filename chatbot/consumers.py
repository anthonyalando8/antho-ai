import json
from channels.generic.websocket import WebsocketConsumer
from main.generate_random_hashed_string import Generator
import base64
from datetime import datetime
from django.core.cache import cache
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from . gemini_model import Model
from . models import ChatHistory

genai = Model()
class ChatConsumer(WebsocketConsumer):
    

    def connect(self):
        
        session_id = self.scope['url_route']['kwargs'].get('session_id')
        print("socket connected with session id: ", session_id)
        self.session_id = session_id
        try:
            self.accept()
        except:
            print("Unable to connect websocket")
    
    def disconnect(self, code):
        print("Socket disconneted from session: ", self.session_id)
        if not self.get_user_from_session(self.session_id):
            try:
                genai.text_models.pop(self.session_id)
            except:
                print("Model doesnt exist in dictionary")
        return super().disconnect(code)
    
    def receive(self, text_data=None, bytes_data=None):

        data_json = json.loads(text_data)

        message_content = data_json["message_content"]

        requested_session_id = message_content.get("session_id")
        message = message_content.get("message")
        base_64_image = message_content.get("image")
        requested_chat_id = message_content.get("request_chat_id")
        # Retrieve the user based on the session ID
        #print(message_content)
        user = self.get_user_from_session(requested_session_id)
        image = None
        if base_64_image:
            image_data = base64.b64decode(base_64_image.split(",")[1])
            image = image_data
        else:
            base_64_image = None
 
        try:
            
            if image:
                res = genai.image_model(user.email if user else requested_session_id, image , message)        
            else:
                if message:
                    genai.set_chat(user.email if user else requested_session_id,[],False)
                    res = genai.text_model(user.email if user else requested_session_id, message)  
                else:
                    self.send_error("Prompt can\'t be empty!")
                    return
                
            prompt_content = {
                "requested_session_id": requested_session_id,
                "requested_chat_id": requested_chat_id,
                "text_prompt": message,
                "image_prompt": image,
                "base_64_image": base_64_image
            }
            
            self.generate_response(res, prompt_content, user)
        except KeyError as e:
            self.send_error("Requested engine does not exists! {}".format(e))
            return
        except:
            self.send_error("Network error occured! Try reloading.")
            return
                
         
    def generate_response(self,model_engine, prompt_content, user):

        message_generated_id = Generator(prompt_content["requested_session_id"])

        context = {
            "message_id":str(message_generated_id),
            "prompt": prompt_content["text_prompt"],
            "res": "",
            "is_first": True,
            "image": prompt_content['base_64_image']
        }
        accumulatedResponse = ""
        try:
            for chunk in model_engine:
                new_chunk = chunk.text
                accumulatedResponse += new_chunk
                context['res'] = accumulatedResponse
                json_data = json.dumps(context)
                context['is_first'] = False
                context['is_on_progress'] = True
                self.send(text_data=json_data)
                
            context = {'is_done':True}   

            self.send(text_data=json.dumps(context))
            # Call the updateHistoryMessage function after processing all chunks
            if user and user.is_authenticated:
                self.updateHistoryMessage(user, accumulatedResponse, prompt_content["base_64_image"] , prompt_content['text_prompt'], prompt_content['requested_chat_id'])

        except Exception as e:
            # Handle any exceptions that occur during the loop
            if prompt_content['base_64_image'] == None:
                last_send, last_received  = genai.get_chat_model(user.email if user else prompt_content["requested_session_id"]).rewind()
            print(f"An error occurred: {e}")
            self.send_error("Something wrong! Trying reloading")
            
            self.send(text_data=json.dumps(context))
            
    
    def send_error(self,error_message):
        context = {
            "is_error": True,
            "error_message": error_message
        }
        self.send(text_data=json.dumps(context))
    
    def get_user_from_session(self,session_id):
        user = None
        try:
            session = Session.objects.get(session_key=str(session_id))
            session_data = session.get_decoded()
            
            user_id = session_data.get('_auth_user_id')

            if user_id:
                user = User.objects.get(id=user_id)
            else:
                print("User not authenticated")

        except Session.DoesNotExist:
            print("Invalid session ID")

        except User.DoesNotExist:
            print("Invalid user ID")

        return user
    
    def updateHistoryMessage(self, user, modelResponse, image, prompt, history_id):
        date = datetime.now().date()
        date_time = datetime.now() 
        current_history = genai.get_chat_model(user.email).history
        new_history_id = Generator(user.email)

        def create_new_history():
            history = ChatHistory(date=date, history_id=new_history_id, current_history=current_history)
            history.save()
            user.chathistory.add(history)
            return new_history_id
        
        if history_id == "new_chat" or not user_has_chat_history(user):
            history_id=create_new_history()
        
        cache.set(f"{user.id}_previous_chat_id", history_id, timeout=86400)
        user_chat_history = ChatHistory.objects.get(user=user,history_id=history_id)

        user_chat_history.current_history = current_history

# Save the object to persist the changes
        user_chat_history.save()
        user_chat_history.messages_set.create(message=prompt, response=modelResponse, date=date_time, 
                                              image=image, request_id=Generator(user.username))

def user_has_chat_history(user):
    user_chat_history_count = ChatHistory.objects.filter(user=user).count()
    return user_chat_history_count > 0


        
        