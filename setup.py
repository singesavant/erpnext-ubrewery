# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

import re, ast

# get version from __version__ variable in ubrewery/__init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('ubrewery/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

requirements = parse_requirements("requirements.txt", session="")
requirements = list(requirements)

setup(
	name='ubrewery',
	version=version,
	description='Micro brewery utilities',
	author='Guillaume Libersat',
	author_email='guillaume@singe-savant.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=[str(ir.requirement) for ir in requirements],
	# dependency_links=[str(ir._link) for ir in requirements if ir._link]
)
