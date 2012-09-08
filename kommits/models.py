from collections import namedtuple
from os.path import join

_Repo = namedtuple('Repo', 'name basepath type baseurl commits')
_Commit = namedtuple('Commit', 'id url user date branch comment')


class Repo(_Repo):

    @property
    def path(self):
        return join(self.basepath, self.name)


class Commit(_Commit):
    pass


