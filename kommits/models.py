from collections import namedtuple
from os.path import join

_Repo = namedtuple('Repo', 'type name basepath baseurl commits')
_Commit = namedtuple('Commit', 'id repo urlpattern user date branch message')


class Repo(_Repo):

    @property
    def path(self):
        return join(self.basepath, self.name)

    @property
    def url(self):
        return join(self.baseurl, self.name)


class Commit(_Commit):
    """TODO: document properly
    urlpattern may use the fields id, repo, user, date and branch and will always
    be joined with the repo baseurl
    """

    @property
    def url(self):
        return join(
            self.repo.baseurl,
            self.urlpattern.format(id=self.id, repo=self.repo, user=self.user, date=self.date, branch=self.branch),
        )


