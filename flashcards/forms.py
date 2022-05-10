from django import forms
from .models import Card


class SearchForm(forms.Form):
    query = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CreateForm(forms.Form):
    query2 = forms.CharField()


class CardForm(forms.ModelForm):
    class Meta:
        Model = Card
        fields = ['group', 'question', 'answer', 'example', 'translation', 'extra']
