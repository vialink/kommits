from sys import stderr
from os import path
from datetime import datetime, timedelta

from jinja2 import Environment, FileSystemLoader

import hgrepo
import gitrepo
try:
    import config
except ImportError as e:
    print >> stderr, 'You should run make to copy the sample config.'
    raise e


BASEDIR = path.dirname(__file__)
J2ENV = Environment()


def render_report(from_date, until_date):
    """Will return a string with the content needed to send to sendmail."""
    withcommits = []
    nocommits = []

    # finding hg commits
    for (basepath, baseurl) in config.HGREPOS:
        repos = hgrepo.find_hg_repos(basepath, baseurl)
        for repo in repos:
            hgrepo.find_hg_commits(repo, from_date, until_date)
            if len(repo.commits) > 0:
                withcommits.append(repo)
            else:
                nocommits.append(repo)

    # finding git commits
    for (basepath, baseurl) in config.GITREPOS:
        repos = gitrepo.find_git_repos(basepath, baseurl)
        for repo in repos:
            gitrepo.find_git_commits(repo, from_date, until_date)
            if len(repo.commits) > 0:
                withcommits.append(repo)
            else:
                nocommits.append(repo)

    l = FileSystemLoader(BASEDIR)
    t = l.load(J2ENV, 'report.html')
    return t.render(withcommits=withcommits, nocommits=nocommits)


def render_email(from_date, until_date):
    """Same as render_report but with email headers."""
    dateformat = '%Y-%m-%d %H:%M:%S'
    header = '\n'.join((
        #'From: noreply@vialink.com.br',
        #'Reply-to: noreply@vialink.com.br',
        #'Return-path: noreply@vialink.com.br',
        'Subject: Commits ({0} to {1})'.format(from_date.strftime(dateformat), until_date.strftime(dateformat)),
        'Content-Type: text/html; charset="utf-8"',
    ))
    return '{0}\n\n{1}'.format(header, render_report(from_date, until_date))


def render_daily_email():
    """Same as render_email but using the last 24h timespan."""
    until_date = datetime.now()
    from_date = until_date - timedelta(days=1)
    return render_email(from_date, until_date)


