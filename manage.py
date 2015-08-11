#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # Dirty hack. Right now, we need this in order for the settings module
    # "mos.settings.devel" to be found (plus many other things that import
    # "mos and its child modules/packages). Ideally we should create a new
    # package "mos" in this directory and move all files there, and then
    # remove this line.
    #sys.path.insert(0, '..')

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mos.settings.devel")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
