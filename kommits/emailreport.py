from sys import stderr
from os import path

from jinja2 import Environment, FileSystemLoader

import hgrepo
try:
    import config
except ImportError as e:
    print >> stderr, 'You should run make to copy the sample config.'
    raise e


BASEDIR = path.dirname(__file__)
J2ENV = Environment()


def render_report(from_date, until_date):
    """Will return a string with the content needed to send to sendmail."""
    #TODO: git repos
    withcommits = []
    nocommits = []
    for (basepath, baseurl) in config.HGREPOS:
        repos = hgrepo.find_hg_repos(basepath, baseurl)
        for repo in repos:
            hgrepo.find_hg_commits(repo, from_date, until_date)
            if len(repo.commits) > 0:
                withcommits.append(repo)
            else:
                nocommits.append(repo)

    l = FileSystemLoader(BASEDIR)
    t = l.load(J2ENV, 'report.html')
    return t.render(withcommits=withcommits, nocommits=nocommits)

