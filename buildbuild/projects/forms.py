from django import forms

class MakeProjectForm(forms.Form):
    name = forms.CharField(max_length = 64, required=True)


