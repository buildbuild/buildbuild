from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="",
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'input-large col-xs-12',
                'placeholder': 'Enter Email'
            }
        )
    )
    password = forms.CharField(
        label="",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input-large col-xs-12',
                'placeholder': 'Enter Password'
            }
        )
    )


class SignUpForm(forms.Form):
    email = forms.EmailField(
        label="",
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'input-large col-xs-12',
                'placeholder': 'Enter Email'
            }
        )
    )
    password = forms.CharField(
        label="",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input-large col-xs-12',
                'placeholder': 'Enter Password'
            }
        )
    )

    password_confirmation = forms.CharField(
        label="",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input-large col-xs-12',
                'placeholder': 'Confirm Your Password'
            }
        )
    )

