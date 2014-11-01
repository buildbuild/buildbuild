from django import forms

class MakeProjectForm(forms.Form):
    
    projects_project_name = forms.CharField(
            max_length = 64,
            required=True,
            label="Project Name",
            )
    
    projects_team_name = forms.CharField(
            max_length = 64,
            required=True,
            label="Team Name",
            )
    
    lang = forms.CharField(
            max_length = 20,
            required=False,
            label="Language"
            )

    ver = forms.CharField(
            max_length = 20,
            required=False,
            label="Language Version"
            )
    
