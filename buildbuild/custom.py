#!/usr/bin/env python
import click
import subprocess
@click.command()
#@click.option('-h', default=1, help='')

def loaddata_set():
    users_fixtures_path = "users/fixtures/users_data.yaml"
    teams_fixtures_path = "teams/fixtures/teams_data.yaml"
    projects_fixtures_path = "projects/fixtures/projects_data.yaml"
    properties_fixtures_path = "properties/fixtures/properties_data.yaml"
    # subprocess.call(data type: list) 
    subprocess.call(
        [
            "python", 
            "manage.py", 
            "loaddata", 
            users_fixtures_path,
            teams_fixtures_path,
            projects_fixtures_path,
            properties_fixtures_path,
        ]
    )
     
if __name__ == '__main__':
    loaddata_set()
