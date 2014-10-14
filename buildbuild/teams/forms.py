from django import forms

class MakeTeamForm(forms.Form):
    name = forms.CharField(max_length = 30, required=True)

   
