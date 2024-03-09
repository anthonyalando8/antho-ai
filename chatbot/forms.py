from django import forms

class CreateChatForm(forms.Form):
    #message = forms.CharField(label="Message")
    message = forms.CharField(widget=forms.Textarea(attrs={"row":"5"}))