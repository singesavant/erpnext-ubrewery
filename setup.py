# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import re, ast

# get version from __version__ variable in ubrewery/__init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('ubrewery/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

setup(
	name='ubrewery',
	version=version,
	description='Micro brewery utilities',
	author='Guillaume Libersat',
	author_email='guillaume@singe-savant.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=parse_requirements('requirements.txt'),

)
