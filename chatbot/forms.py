from django import forms

class CreateChatForm(forms.Form):
    message = forms.CharField(label="Message")