# -*- coding: utf8 -*-

from setuptools import setup

setup(
    name='githubhook',
    version='0.5',
    packages=['githubhook'],
    license='MIT License',
    keywords='git github webhook webhooks',
    description='Bind GitHub WebHooks to actions',
    install_requires=['docopt'],
    author='William Tisäter',
    author_email='william@defunct.cc',
    url='https://github.com/tiwilliam/githubhook',
    entry_points={
        'console_scripts': ['githubhook = githubhook:run'],
    }
)
