from setuptools import setup, find_packages

setup(

	author='ihsan',
	name='twitter',
	version='1.1.0',
	packages=find_packages(),
	author_email='ihsanl@pm.me',
	description='Twitter scraper, streamer',
	url='https://github.com/ihsanturk/twitter',
	entry_points={'console_scripts': ['twitter = twitter.cli:main']},
	install_requires=['pymongo', 'twint @ git+https://github.com/twintproject/twint.git@origin/master#egg=twint', 'docopt', 'nest_asyncio'],

)
