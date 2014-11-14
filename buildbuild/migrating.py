#!/usr/bin/env python
import click
import subprocess
@click.command()
#@click.option('-h', default=1, help='')

# Scenario
# makemigrations -> migrate
def migrating_set():
    # subprocess.call(data type: list) 
    # migrating from users -> teams -> projects 
    #( It is important because MtoM relationship)
    subprocess.call(
        [
            "python", 
            "manage.py", 
            "makemigrations",
            "users",
            "teams",
            "projects",
        ]
    )
   
    # for remain apps' fields
    subprocess.call(
        [
            "python", 
            "manage.py", 
            "makemigrations",
        ]
    )

    # for remain apps' fields
    subprocess.call(
        [
            "python",
            "manage.py",
            "migrate", 
        ]
    )



if __name__ == '__main__':
    migrating_set()
