from collections import namedtuple

_Repo = namedtuple('Repo', 'name path type baseurl commits')
_Commit = namedtuple('Commit', 'id url user date branch comment')


class Repo(_Repo):
    pass


class Commit(_Commit):
    pass


