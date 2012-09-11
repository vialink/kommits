from os import path, listdir
from datetime import datetime

from mercurial import ui, hg, util
from mercurial.node import short
import git

from models import Repo, Commit


def find_git_repos(basepath, baseurl=''):
    """Returns a list of hg Repos in basepath"""
    def _find_repos(_path, name):
        if not path.isdir(_path):
            return []
        ret = []
        subdir = listdir(_path)
        if '.git' not in subdir and not _path[-4:] == '.git':
            for r in subdir:
                reponame =  '{0}/{1}'.format(name, r) if name else r
                ret.extend(_find_repos(path.join(_path, r), reponame))
        else:
            ret.append(Repo(
                type='git',
                name=name,
                basepath=basepath,
                baseurl=baseurl,
                commits=[],
            ))
        return ret
    return _find_repos(basepath, '')


def find_git_commits(repo, from_date, until_date):
    """Initializes repo.commits with all commits between the given dates"""
    if from_date > until_date:
        # this should be impossible, maybe we should
        # raise an exception to indicate missuse
        return []

    #TODO: optimize
    gitrepo = git.Repo(repo.path)
    commits = [c for c in gitrepo.iter_commits(all=True)]

    # helper function to get branch from git.Commit
    branch = lambda c: gitrepo.git.branch(contains=c.hexsha).split('\n')[0][2:]
    # helper function to get datetime from git.Commit
    when = lambda c: datetime.fromtimestamp(c.committed_date)
    # helper function to get Commit from git.Commit
    com = lambda c: Commit(
        id=c.hexsha,
        repo=repo,
        urlpattern='?p={repo.name};a=commit;h={id}',
        #urlpattern='{repo.name}/commit/?id={id}'
        user=c.author.name,
        date=when(c),
        #XXX: in git a commit may be in more than one branch
        # we are choosing the first we find it in.
        branch=branch(c),
        message=c.summary,
    )
    # filter on date
    repo.commits.extend([com(c) for c in commits if from_date < when(c) < until_date])

