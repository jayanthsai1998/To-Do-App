from django import forms
from django.forms import TextInput, PasswordInput, SelectDateWidget, Select
from todolistapp.models import *
from datetime import date


class ToDoListForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        exclude = ['id', 'user']
        widgets = {
            'name': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'TODO list name', 'label': 'Name'}
            )
        }


class ToDoListItemForm(forms.ModelForm):
    class Meta:
        model = ToDoListItem
        exclude = ['id', 'todolist', 'date_created']
        widgets = {
            'content': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'TODO list item content', 'label': 'Content'}
            )
        }


class SignUpForm(forms.Form):
    first_name = forms.CharField(
        max_length=75,
        required=True,
        widget=TextInput(
            attrs={'class': 'form-control', 'placeholder': 'First name', 'label': 'First Name'}
        )
    )
    last_name = forms.CharField(
        max_length=75,
        required=True,
        widget=TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Last name', 'label': 'Last Name'}
        )
    )
    username = forms.CharField(
        max_length=75,
        required=True,
        widget=TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username', 'label': 'Username'}
        )
    )
    password = forms.CharField(
        required=True,
        widget=PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password', 'label': 'Password'}
        )
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=75,
        required=True,
        widget=TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username', 'label': 'Username'}
        )
    )
    password = forms.CharField(
        required=True,
        widget=PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password', 'label': 'Password'}
        )
    )