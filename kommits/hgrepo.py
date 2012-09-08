from os import path, listdir

from mercurial import ui, hg, util
from mercurial.node import short

from models import Repo, Commit


def find_hg_repos(repopath):
    """Returns a list of hg Repos in repopath"""
    def _find_repos(repopath, name):
        if not path.isdir(repopath):
            return []
        ret = []
        subdir = listdir(repopath)
        if '.hg' not in subdir:
            for r in subdir:
                reponame =  '{0}/{1}'.format(name, r) if name else r
                ret.extend(_find_repos( path.join(repopath, r), reponame))
        else:
            ret.append(Repo(
                name=name,
                path=repopath,
                type='hg',
                baseurl='',
                commits=[],
            ))
        return ret
    return _find_repos(repopath, '')


def find_commits(repo, from_date, until_date):
    """Initializes repo.commits with all commits between the given dates"""
    pass

