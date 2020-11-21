from setuptools import setup, find_packages

setup(

	author='ihsan',
	name='twitter',
	version='0.0.1',
	packages=find_packages(),
	author_email='ihsanl@pm.me',
	description='Twitter scraper, streamer',
	url='https://github.com/ihsanturk/twitter',
	install_requires=['pymongo', 'twint', 'docopt'],
	entry_points={'console_scripts': ['twitter = twitter.cli:main']},

)
