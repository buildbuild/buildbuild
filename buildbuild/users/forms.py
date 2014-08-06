from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(max_length = 50)
    password = forms.CharField(widget=forms.PasswordInput)
