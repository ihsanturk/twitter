from setuptools import setup

setup(
    name='twitter',
    version="0.2.0",
    py_modules=['twitter'],
    entry_points={
        'console_scripts': [
            'twitter = cli:main',
        ],
    }
)
