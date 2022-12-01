from django import forms
# from mdeditor.fields import MDTextField

from .models import Essay


class EssayForm(forms.ModelForm):
    class Meta:
        model = Essay
        fields = ['title', 'tags', 'content']
        labels = {
            'title': '标题',
            'tags': '标签',
            'content': '正文，可使用markdown语法'}
        # widgets = {'content': MDTextField}
