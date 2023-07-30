#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import environ

environ.Env()
environ.Env.read_env(env_file="bgs/.env")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bgs.settings')
    try:
        from django.core.management import execute_from_command_line

        # Set the port number from .env (or "3000" if non-existent or invalid)
        from django.core.management.commands.runserver import Command as runserver
        try:
            port = os.environ["PORT"]
            runserver.default_port = port if port.isnumeric() else "3000"
        except Exception as e:
            runserver.default_port = "3000"


    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
