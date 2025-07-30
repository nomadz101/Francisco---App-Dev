from django import forms
from .models import InventoryItem

class InventoryForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'description', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity', 'description']