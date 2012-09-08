import unittest
from os import path, system
from datetime import datetime, timedelta

import models
import hgrepo


class TestHGRepo(unittest.TestCase):
    """Testing correctness of the hgrepo module."""

    def setUp(self):
        """Create a few example repos. Should create some commits."""
        self.reponames = ['repoA', 'repoB', 'reps/repoC']
        self.repobase = 'hgrepos'
        # create repos
        for name in self.reponames:
            repopath = path.join(self.repobase, name)
            # create repo dir
            system('mkdir -p {0}'.format(repopath))
            # init hg on this repo
            system('cd {0} && hg init'.format(repopath))
        # commit some stuff
        self.phonycommits = ['Some initial commit.', 'Doing some stuff.', 'Another commit message.']
        self.phonyrepo = models.Repo(type='hg', name = self.reponames[0], basepath=self.repobase, baseurl='https://hg.foo.bar/repos/', commits=[])
        self.phonyuser = 'johndoe'
        for (i, commit) in enumerate(self.phonycommits):
            system('cd {0} && touch file{1} && hg add > /dev/null && hg commit -m"{2}" -u {3}'.format(self.phonyrepo.path, i, commit, self.phonyuser))

    def tearDown(self):
        """Remove all examples repos, it uses rm -rf, may be dangerous."""
        system('rm -rf {0}'.format(self.repobase))

    def test_finder(self):
        """Test if repos created in setUp are found."""
        repos = hgrepo.find_hg_repos(self.repobase)
        reponames = []
        for repo in repos:
            reponames.append(repo.name)
        self.assertEqual(set(reponames), set(self.reponames))

    def test_commits(self):
        """Test if commits created in setUp are found."""
        repo = self.phonyrepo
        until_date = datetime.now()
        from_date = until_date - timedelta(hours=2)
        hgrepo.find_hg_commits(repo, from_date, until_date)
        commits = []
        for commit in repo.commits:
            commits.append(commit.message)
        while len(repo.commits) > 0:
            repo.commits.pop()
        self.assertEqual(set(commits), set(self.phonycommits))

    def test_commiturls(self):
        """Test wether commit urls are generated properly. This depends on the previous test."""
        repo = self.phonyrepo
        until_date = datetime.now()
        from_date = until_date - timedelta(hours=2)
        hgrepo.find_hg_commits(repo, from_date, until_date)
        commit = repo.commits[0]
        while len(repo.commits) > 0:
            repo.commits.pop()
        expected_url = 'https://hg.foo.bar/repos/repoA/rev/1'
        self.assertEqual(expected_url, commit.url)



if __name__ == '__main__':
    unittest.main()

