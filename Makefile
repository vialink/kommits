all: samples depend

depend:

	@@pip install -r requirements.txt

test:

	@@python kommits/tests.py

docs:

	pycco kommits/*.py

samples: kommits/config.py

kommits/config.py:

	@@cd kommits && [ -f config.py ] || cp config.py.sample config.py

