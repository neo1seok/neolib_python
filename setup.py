import sys
sys.path.insert(0, 'neolib')
import neolib
currentVersion = neolib.__version__

from distutils.core import setup
setup(
	name = 'neolib',
	packages=['neolib',
				'neolib.crypto',
			  'sample'
			  #'neolib.compress',

		],
	version = currentVersion,
	description = 'useful library 4 python developing',
	author = 'neo1seok',
	author_email = 'neo1seok@gmail.com',
	keywords = ['neolib', 'neo1seok'],
	classifiers = [
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Natural Language :: English",
		"License :: neo1seok licnese",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.3",
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: 3.5"
	]
)
