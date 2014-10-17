from django import forms

class MakeTeamForm(forms.Form):
    teams_team_name = forms.CharField(max_length = 64, required=True)

   
