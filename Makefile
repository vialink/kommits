all: samples

test:

	@@python kommits/tests.py

samples: kommits/config.py

kommits/config.py:

	@@cd kommits && [ -f config.py ] || cp config.py.sample config.py

