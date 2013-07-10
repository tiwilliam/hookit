from setuptools import setup

setup(
    name='githook',
    version='0.1',
    packages=['githook'],
    license='MIT License',
    keywords='git github webhook webhooks',
    description='Bind GitHub WebHooks to actions',
    install_requires=['docopt'],
    author='William Tisäter',
    author_email='william@defunct.cc',
    url='https://github.com/tiwilliam/githook',
    entry_points={
        'console_scripts': ['githook = githook:cmd'],
    }
)
