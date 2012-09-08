import unittest
from os import path, system

import models
import hgrepo


class TestHGRepo(unittest.TestCase):

    def setUp(self):
        """Create a few example repos. Should create some commits."""
        self.reponames = ['repoA', 'repoB', 'reps/repoC']
        self.repobase = 'hgrepos'
        for name in self.reponames:
            repopath = path.join(self.repobase, name)
            # create repo dir
            system('mkdir -p {0}'.format(repopath))
            # init hg on this repo
            system('cd {0} && hg init'.format(repopath))

    def tearDown(self):
        """Remove all examples repos, it uses rm -rf, may be dangerous."""
        system('rm -rf {0}'.format(self.repobase))

    def test_finder(self):
        """Test if repos created in setUp are found by hgrepo module."""
        repos = hgrepo.find_hg_repos(self.repobase)
        reponames = []
        for repo in repos:
            reponames.append(repo.name)
        self.assertEqual(set(reponames), set(self.reponames))


if __name__ == '__main__':
    unittest.main()

