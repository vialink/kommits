from os import path, listdir
from datetime import datetime

from mercurial import ui, hg, util
from mercurial.node import short

from models import Repo, Commit


def find_hg_repos(basepath, baseurl=''):
    """Returns a list of hg Repos in basepath"""
    def _find_repos(basepath, name):
        if not path.isdir(basepath):
            return []
        ret = []
        subdir = listdir(basepath)
        if '.hg' not in subdir:
            for r in subdir:
                reponame =  '{0}/{1}'.format(name, r) if name else r
                ret.extend(_find_repos( path.join(basepath, r), reponame))
        else:
            ret.append(Repo(
                type='hg',
                name=name,
                basepath=basepath,
                baseurl=baseurl,
                commits=[],
            ))
        return ret
    return _find_repos(basepath, '')


def find_hg_commits(repo, from_date, until_date):
    """Initializes repo.commits with all commits between the given dates"""
    if from_date > until_date:
        # this should be impossible, maybe we should
        # raise an exception to indicate missuse
        return []

    hgrepo = hg.repository(ui.ui(), repo.path)
    changes = hgrepo.changelog

    ctx = lambda c: hgrepo.changectx(c)
    # helper function to get datetime from change
    when = lambda ctx: datetime.fromtimestamp(ctx.date()[0])
    # helper function to get Commit from change
    com = lambda ctx: Commit(
        id=ctx.rev(),
        repo=repo,
        urlpattern='{repo.name}/revs/{id}',
        user=ctx.user(),
        date=when(ctx),
        branch=ctx.branch(),
        message=ctx.description(),
    )
    # filter on date
    repo.commits.extend([com(ctx(c)) for c in changes if from_date < when(ctx(c)) < until_date])

