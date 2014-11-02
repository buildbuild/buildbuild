from django import forms

class MakeTeamForm(forms.Form):
    teams_team_name = forms.CharField(
                          label="Team Name",
                          max_length = 64, 
                          required=True
                      )

   
