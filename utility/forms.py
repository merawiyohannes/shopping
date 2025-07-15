from django import forms
from item.models import Category, Item
CLASS_VAR = 'px-4 py-2 rounded-xl w-full border border-black'


class EditForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['category', 'name', 'description', 'price', 'quantity', 'images', 'created_by', 'is_sold']
        
        
        widgets = {
            
            "category": forms.Select(attrs={
                "id":"category",
                "class":CLASS_VAR
            }),
            
            "created_by": forms.Select(attrs={
                "id":"created_by",
                "class":CLASS_VAR
            }),
            
            "name": forms.TextInput(attrs={
                "placeholder":"name of item",
                "id":"name",
                "class":CLASS_VAR
            }),
            
            "description": forms.Textarea(attrs={
                "placeholder":"description...",
                "id":"description",
                "class": f"{CLASS_VAR} h-12 resize-none align-top"
            }),
            
            "price": forms.NumberInput(attrs={
                "placeholder":"$ price",
                "id":"price",
                "class":CLASS_VAR
            }),
            
            "quantity": forms.NumberInput(attrs={
                "placeholder":"Quantity",
                "id":"quantity",
                "class":CLASS_VAR
            }),
            
            "images": forms.ClearableFileInput(attrs={
                "id":"images",
                "class":CLASS_VAR
            }),
        }

class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['category', 'name', 'description', 'price', 'quantity', 'images', 'created_by']
        
        widgets = {
            
            "category": forms.Select(attrs={
                "id":"category",
                "class":CLASS_VAR
            }),
            
            "created_by": forms.Select(attrs={
                "id":"created_by",
                "class":CLASS_VAR
            }),
            
            "name": forms.TextInput(attrs={
                "placeholder":"name of item",
                "id":"name",
                "class":CLASS_VAR
            }),
            
            "description": forms.Textarea(attrs={
                "placeholder":"description...",
                "id":"description",
                "class": f"{CLASS_VAR} h-12 resize-none align-top"
            }),
            
            "price": forms.NumberInput(attrs={
                "placeholder":"$ price",
                "id":"price",
                "class":CLASS_VAR
            }),
            
            "quantity": forms.NumberInput(attrs={
                "placeholder":"Quantity",
                "id":"quantity",
                "class":CLASS_VAR
            }),
            
            "images": forms.ClearableFileInput(attrs={
                "id":"images",
                "class":CLASS_VAR
            }),
        }