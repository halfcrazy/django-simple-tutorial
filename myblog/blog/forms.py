from django import forms

from .models import BlogPost


class PostForm(forms.ModelForm):
    title = forms.CharField(label='标题',
                            max_length=200)
    body = forms.CharField(label='正文',
                           widget=forms.Textarea)

    class Meta:
        model = BlogPost
        fields = ('title', 'body')
