from setuptools import setup

setup(
    name='twitter',
    version="2.0.1-alpha",
    py_modules=['twitter'],
    packages = ['twitter'],
    entry_points={
        'console_scripts': [
            'twitter = twitter.cli:main',
        ],
    }
)
