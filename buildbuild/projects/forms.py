from django import forms

class MakeProjectForm(forms.Form):
    # Make project should be implemented in team page,
    # not in form field
    # team name automatically need to be set

    projects_project_name = forms.CharField(
            max_length = 64,
            required=True,
            label="Project Name",
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
    
