Kommits
=======

Generate HTML from daily commits in several Git or Hg repositories.

Installation
------------

Just copy this project to any folder in your computer.

Configuration
-------------

Copy `kommits/config.py.sample` and fill with your repositories.

Usage
-----

Print HTML in your terminal:

    ./report.py

Or you can send it to your mail:

	./report.py | /usr/sbin/sendmail -f from@domain.com -i to@domain.com

Or put it on crontab:

	55 23 * * * LANG=en_US.UTF-8 /path/to/kommits/report.py | /usr/sbin/sendmail -f from@domain.com -i to@domain.com 2>&1

