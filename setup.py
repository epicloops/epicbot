#!/usr/bin/env python
import os
import codecs
import re

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

readme = open('README.md').read()

setup(
    name='epicbot',
    version=find_version('epicbot', '__init__.py'),
    description='Epic web crawler.',
    long_description=readme,
    author='A.J. Welch',
    author_email='awelch0100@gmail.com',
    url='https://github.com/epicloops/epicbot',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = epicbot.settings']},
    include_package_data=True,
    install_requires=[
        'epiclib',
        'Scrapy',
        'scrapylib',
        'pyechonest',
        'boto',
        'SQLAlchemy',
        'psycopg2',
    ],
)
