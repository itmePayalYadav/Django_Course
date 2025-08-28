from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter the title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Write your content here',
                'rows': 5
            }),
        }
    
    def clean(self):
        data = self.cleaned_data
        title = data.get('title')
        content = data.get('content') 

        qs = Article.objects.filter(title__icontains=title, content__icontains=content)
        if qs.exists():
            self.add_error("title", f"{title} is already in use")
        return data
