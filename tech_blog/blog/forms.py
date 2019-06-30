from django import forms
from . import models

class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ('author', 'title', 'text')

        widgets = {
            'title' : forms.TextInput(attrs = {'class' : 'text-input'}),
            'text' : forms.Textarea(attrs = {'class' : 'editable medium-editor-textarea post-content'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('author', 'text')

        widgets = {
            'author' : forms.TextInput(attrs = {'class' : 'text-input'}),
            'text' : forms.Textarea(attrs = {'class' : 'editable medium-editor-textarea post-content'})
        }