# -*- coding: utf8 -*-

from setuptools import setup

setup(
    name='githubhooks',
    version='0.5',
    packages=['githubhooks'],
    license='MIT License',
    keywords='git github webhook webhooks',
    description='Bind GitHub WebHooks to actions',
    install_requires=['docopt'],
    author='William Tisäter',
    author_email='william@defunct.cc',
    url='https://github.com/tiwilliam/githubhooks',
    entry_points={
        'console_scripts': ['githubhooks = githubhooks:run'],
    }
)
