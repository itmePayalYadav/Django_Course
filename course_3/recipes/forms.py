from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'directions']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter the recipe name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Write a short description',
                'rows': 3
            }),
            'directions': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Step-by-step cooking instructions',
                'rows': 5
            }),
        }
