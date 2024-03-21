#!/bin/bash
python manage.py collectstatic && gunicorn --workers MamaPesa.wsgi