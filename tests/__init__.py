# -*- coding: utf-8 -*-


import os
import sys
import fnmatch
import subprocess


URL = 'http://localhost:5000'
PYRESTTEST = os.path.join(__path__[0], '../venv/bin/pyresttest')
if not os.path.exists(PYRESTTEST):
	PYRESTTEST = 'pyresttest'


def run(resource=None):
	if not resource:
		run_all()
		return

	test = os.path.join(__path__[0], resource.replace('.', '/')) + '.yaml'
	command_run(test)


def run_all():
	tests = []
	for root, dirnames, filenames in os.walk(__path__[0]):
		for filename in fnmatch.filter(filenames, '*.yaml'):
			tests.append(os.path.join(root, filename))
	for t in tests:
		command_run(t)


def command_run(test_file):
	subprocess.call([PYRESTTEST, URL, test_file])

