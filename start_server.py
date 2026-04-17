#!/usr/bin/env python
import os
import sys
import time
import threading

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geopram_tech.settings")

from django.core.management import execute_from_command_line


def run_server():
    execute_from_command_line(
        ["manage.py", "runserver", "127.0.0.1:6500", "--noreload"]
    )


if __name__ == "__main__":
    run_server()
