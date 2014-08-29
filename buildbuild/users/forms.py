from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(max_length = 50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class SignUpForm(forms.Form):
    email = forms.EmailField(max_length = 50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
        
