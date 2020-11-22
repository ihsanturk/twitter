from setuptools import setup, find_packages

setup(

	author='ihsan',
	name='twitter',
	version='1.0.0',
	packages=find_packages(),
	author_email='ihsanl@pm.me',
	description='Twitter scraper, streamer',
	url='https://github.com/ihsanturk/twitter',
	entry_points={'console_scripts': ['twitter = twitter.cli:main']},
	install_requires=['pymongo', 'twint @ git+git://github.com/twintproject/twint@ae5e7e1189be1cf319bbd55b921aca6bfb899f8c', 'docopt'],

)
