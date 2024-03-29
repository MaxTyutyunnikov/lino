#!/usr/bin/env python
import os
import sys

# we add ".." to PYTHONPATH because this is a single-dir Django project
sys.path.insert(0,'..')

if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "watch_tutorial.settings"

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
