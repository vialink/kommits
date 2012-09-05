#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time
from datetime import datetime, timedelta
from subprocess import Popen, PIPE

from hg_util import repository_to_table

#---

base = '/Users/jan/Projects'
end = datetime.now()
start = end - timedelta(days=1)

#---

def search_repos(reponame, repodir):
    if not os.path.isdir(repodir):
        return []
    subdir = os.listdir(repodir)
    ret = []
    if '.hg' not in subdir:
        for r in subdir:
            ret.extend(search_repos('%s/%s' % (reponame, r), os.path.join(repodir, r)))
    else:
        ret.append(tuple([ reponame, repodir ]))
    return ret

#regexp = [
#    (re.compile(r'^(changeset:\s+[0-9]+:)([a-zA-Z0-9]+)', flags=re.MULTILINE), r'<a href="">\1\2</a>'),
#]

repos = search_repos('', base)
repos.sort()
format = '%Y-%m-%d %H:%M:%S'
daterange = '%s to %s' % (start.strftime(format), end.strftime(format))
nocommits = []
content = []
for r in repos:
    #args = ['/usr/bin/hg', 'log', '--date', daterange, r[1]]
    #proc = Popen(args, stdout=PIPE, stderr=PIPE)
    #out, err = proc.communicate()

    out = repository_to_table(r[0][1:], r[1], date=time.mktime(start.timetuple()))
    if out:
        #for pattern, repl in regexp:
        #    out = re.sub(pattern, repl, out)
        content.append('<p>')
        content.append('<b>%s</b>' % r[0])
        content.append(out)
        content.append('</p>')
    else:
        nocommits.append(r[0])
nocommits.sort()

headers = [
    #'From: noreply@vialink.com.br',
    #'Reply-to: noreply@vialink.com.br',
    #'Return-path: noreply@vialink.com.br',
    'Subject: Commits (%s)' % daterange,
    'Content-Type: text/html; charset="utf-8"',
]

print '\n'.join(headers)
print ''
print '\n'.join(content)
print '<p>'
print '<b>No commits:</b>'
print '<ul>'
for c in nocommits:
    print '<li>%s</li>' % c
print '</ul>'
print '</p>'

