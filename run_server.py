#!/usr/bin/env python
import os
import sys
import subprocess

os.chdir('backend')
sys.exit(subprocess.call([sys.executable, 'manage.py', 'runserver']))
