from os import path, listdir

from mercurial import ui, hg, util
from mercurial.node import short

from models import Repo, Commit


def find_hg_repos(basepath):
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
                name=name,
                basepath=basepath,
                type='hg',
                baseurl='',
                commits=[],
            ))
        return ret
    return _find_repos(basepath, '')


def find_hg_commits(repo, from_date, until_date):
    """Initializes repo.commits with all commits between the given dates"""
    pass

