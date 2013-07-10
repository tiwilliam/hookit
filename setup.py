# -*- coding: utf8 -*-

from setuptools import setup

setup(
    name='hookit',
    version='0.5',
    packages=['hookit'],
    license='MIT License',
    keywords='git github webhook webhooks',
    description='Bind GitHub WebHooks to actions',
    install_requires=['docopt'],
    author='William Tisäter',
    author_email='william@defunct.cc',
    url='https://github.com/tiwilliam/hookit',
    entry_points={
        'console_scripts': ['hookit = hookit:run'],
    }
)
