#!/usr/bin/env python
# -*- coding: utf-8 -*-

# URL: http://stackoverflow.com/questions/1918417/retrieving-logs-from-mercurial-using-api
# Changes by msbrogli

import os, sys, datetime, time

from mercurial import ui, hg, util
from mercurial.node import short

def find_repository(name):
    base = '/usr/local/systems/hg/repos/'
    path = os.path.join(base, name)

    repos = hg.repository(ui.ui(), path)
    return repos

def find_changes(repos, branch, date):

    # returns true if d2 is newer than d1
    def newerDate(d1, d2):
         d1 = datetime.datetime.fromtimestamp(d1)
         d2 = datetime.datetime.fromtimestamp(d2)
         return d1 < d2

    changes = repos.changelog

    out = []
    # filter on branch
    if branch != '':
        changes = [change for change in changes if repos.changectx(change).branch() == branch ]

    # filter on date
    if date != '':
        changes = [change for change in changes if newerDate(date, repos.changectx(change).date()[0]) ]

    return changes

#_element('title', str(change.rev()))
#_element('description', change.description())
#_element('guid', str(change.rev()))
#_element('author', change.user())
#_element('link', link)
#_element('pubdate', str(datetime.datetime.fromtimestamp(change.date()[0])))
def print_table(changes, repos, template):
    if len(changes) == 0:
        return ''
    ret = []
    ret.append('<table border="1">')
    for change in changes:
        ctx = repos.changectx(change)
        link = template % {'node': short(ctx.node())}
        ret.append('<tr>')
        ret.append('<td><a href="%s">%s:%s</a></td>' % (link, str(ctx.rev()), short(ctx.node())))
        ret.append('<td>%s</td>' % ctx.user())
        ret.append('<td>%s</td>' % str(datetime.datetime.fromtimestamp(ctx.date()[0])))
        ret.append('<td>%s</td>' % ctx.branch())
        ret.append('<td>%s</td>' % ctx.description().replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
        ret.append('</tr>')
        #print >>sys.stderr, ctx.description()
    ret.append('</table>')
    return '\n'.join(ret)

def repository_to_table(reponame, repodir, branch='', date=None):
    repos = find_repository(repodir)
    changes = find_changes(repos, branch, date)
    rev_link_template = 'https://hg.vialink.com.br/%(repos)s/rev/%%(node)s' % {
        'repos': reponame
        }
    return print_table(changes, repos, rev_link_template)

