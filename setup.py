# -*- coding: utf8 -*-

from hookit import VERSION
from setuptools import setup

setup(
    name='hookit',
    version=VERSION,
    packages=['hookit'],
    license='MIT License',
    keywords='git github webhook webhooks',
    description='Bind GitHub WebHooks to actions',
    install_requires=['docopt >= 0.6.0', 'github3.py >= 0.9.0', 'ipaddress >= 1.0.6'],
    author='William Tisäter',
    author_email='william@defunct.cc',
    url='https://github.com/tiwilliam/hookit',
    entry_points={
        'console_scripts': ['hookit = hookit:run'],
    }
)
