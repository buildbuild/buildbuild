from django import forms

class MakeTeamForm(forms.Form):
    teams_team_name = forms.CharField(
                          label="Team Name",
                          max_length = 64, 
                          required=True,
                          widget=forms.TextInput(
                              attrs={
                                  'class': 'input-large col-xs-12',
                                  'placeholder': 'Enter Name'
                              }
                          )
                      )
    
    teams_contact_number = forms.CharField(
                               label = "Contact number",
                               max_length = 20,
                               required=False,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'input-large col-xs-12',
                                       'placeholder': 'Enter Contact Number ( Optional )'
                                   }
                               )
                           )

    teams_team_url = forms.URLField(
                        label = "Team URL",
                        required = False,
                        widget=forms.TextInput(
                            attrs={
                                'class': 'input-large col-xs-12',
                                'placeholder': 'Enter Team site ( Optional )'
                            }
                        )
                     )
    
