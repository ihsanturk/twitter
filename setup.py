from setuptools import setup

setup(
    name='twitter',
    version="2.1.0",
    py_modules=['twitter'],
    packages = ['twitter'],
    entry_points={
        'console_scripts': [
            'twitter = twitter.cli:main',
        ],
    }
)
