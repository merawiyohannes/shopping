from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        
    text = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder":"type message...",
        "class":"rounded-xl px-5 py-3"
    }))