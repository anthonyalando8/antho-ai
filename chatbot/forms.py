from django import forms
from .models import Chat

class CreateChatForm(forms.ModelForm):
    #message = forms.CharField(label="Message")
    class Meta:
        model = Chat
        fields = ["image", "message"]
        widgets = {
            'message': forms.Textarea(attrs={'placeholder': 'Enter message',  
                                             'class': 'form-control bg-transparent text-light border-0', 
                                             'aria-describedby':"basic-addon1",
                                             'id':"id_message"}),
            'image': forms.FileInput(attrs={'class': 'form-control-file image-input'}),
        }
    def __init__(self, *args, **kwargs):
        super(CreateChatForm, self).__init__(*args, **kwargs)

        # Set required attribute for fields (True or False)
        self.fields['message'].required = False
        self.fields['message'].label = '' 
        self.fields['image'].required = False
