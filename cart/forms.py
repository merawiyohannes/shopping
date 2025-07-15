from django import forms
from .models import CheckOutOrder

CLASS_INPUT = "px-3 py-2 rounded-xl w-full border-black border"

class QuickForm(forms.Form):
    pass

class CheckOutForm(forms.ModelForm):
    
    class Meta:
        model = CheckOutOrder
        fields = ("name", 'phone', 'email')
    name = forms.CharField(widget=forms.TextInput(attrs={
        "id":"name",
        "placeholder":"Enter Your Name...",
        "class":CLASS_INPUT
    }))
    
    phone = forms.CharField(widget=forms.TextInput(attrs={
        "id":"phone",
        "placeholder":"Phone Number",
        "class":CLASS_INPUT
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "id":"email",
        "placeholder":"Email Adress",
        "class":CLASS_INPUT
    }))

