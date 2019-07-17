'''Test the match.py file.'''

import pytest
from collections import namedtuple
from itertools import zip_longest

from hydrate.component import Component
from hydrate.match import Matcher


FILE = 'hydrate.match'


class TestMatcher():
    '''Test suite for the Matcher class.'''

    tst_repo_components = [Component(name="dep1-dep2"),
                           Component(name="dep3"),
                           Component(name="dep4-dep5"),
                           Component(name="dep6-dep7")]
    tst_matcher = Matcher(tst_repo_components)
    tst_cluster_components = [Component(name="dep1"),
                              Component(name="dep2"),
                              Component(name="dep3"),
                              Component(name="dep4"),
                              Component(name="dep6")]

    exp_full_matches = [Component(name="dep1-dep2"),
                        Component(name="dep3")]
    exp_fm_leftovers = [Component(name="dep4"),
                        Component(name="dep6")]
    exp_partial_matches = [Component(name="dep6")]
    exp_pm_leftovers = []
    exp_no_matches = []

    def test_init(self):
        '''Test the __init__ method.'''
        assert self.tst_matcher.repo_components == self.tst_repo_components

    def test_match_components(self):
        '''Test the match_components method.'''
        pass

    param_get_start_index = [[1, 1, 2], [-1, -1, -2], [0, 0, 0]]
    @pytest.mark.parametrize('tst_len, tst_prev_index, exp_start_index',
                             param_get_start_index)
    def test_get_start_index(self, mocker, tst_len, tst_prev_index, exp_start_index):
        '''Test the get_start_index method.'''
        mocker.patch(f'{FILE}.len', return_value=tst_len)
        MatchCategory = namedtuple('MatchCategory',
                                   ['category', 'start_index', 'subcomponents'])
        self.tst_matcher.match_categories = [MatchCategory(category='test_category',
                                                           start_index=tst_prev_index,
                                                           subcomponents=None)]

        start_index = self.tst_matcher.get_start_index()

        assert start_index == exp_start_index


    @pytest.mark.parametrize('''repo_components, cluster_components,
                            expected_fm, expected_leftos''',
                         [(tst_repo_components,
                           tst_cluster_components,
                           exp_full_matches,
                           exp_fm_leftovers)])
    def test_get_full_matches(self, repo_components, cluster_components,
                              expected_fm, expected_leftos):
        """Test the get_full_matches method."""

        fm_results = self.tst_matcher.get_full_matches(cluster_components)

        fms = fm_results.full_matches
        leftovers = fm_results.leftovers

        for fmc, exp in zip_longest(fms, expected_fm):
            assert fmc.name == exp.name

        for lefto, exp_lefto in zip_longest(leftovers, expected_leftos):
            assert lefto.name == exp_lefto.name

    def test_get_partial_matches(self):
        '''Test the get_partial_matches method.'''
        pass