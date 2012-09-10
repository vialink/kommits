#!/usr/bin/env python
from kommits import report

if __name__ == '__main__':
    print report.render_daily_email().encode('utf-8')

