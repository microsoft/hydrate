"""Test the match.py file."""

import pytest
from collections import namedtuple
from itertools import zip_longest

from hydrate.component import Component
from hydrate.match import Matcher


FILE = 'hydrate.match'


class TestMatcher():
    """Test suite for the Matcher class."""

    tst_repo_components = [Component(name="dep1-dep2"),
                           Component(name="dep3"),
                           Component(name="dep4-dep5"),
                           Component(name="dep6-dep7")]
    tst_matcher = Matcher(tst_repo_components)
    tst_cluster_components = [Component(name="dep1"),
                              Component(name="dep2"),
                              Component(name="dep3"),
                              Component(name="dep4"),
                              Component(name="dep6"),
                              Component(name="dep8")]

    exp_full_matches = [Component(name="dep1-dep2"),
                        Component(name="dep3")]
    exp_fm_leftovers = [Component(name="dep4"),
                        Component(name="dep6"),
                        Component(name="dep8")]
    exp_partial_matches = [Component(name="dep4-dep5"),
                           Component(name="dep6-dep7")]
    exp_pm_no_matches = [Component(name="dep8")]
    exp_no_matches = [Component(name="dep8")]

    def test_init(self):
        """Test the __init__ method."""
        assert self.tst_matcher.repo_components == self.tst_repo_components

    def test_match_components(self):
        """Test the match_components method."""
        pass

    param_get_start_index = [[1, 1, 2], [-1, -1, -2], [0, 0, 0]]
    @pytest.mark.parametrize('tst_len, tst_prev_index, exp_start_index',
                             param_get_start_index)
    def test_get_start_index(self, mocker, tst_len, tst_prev_index, exp_start_index):
        """Test the get_start_index method."""
        mocker.patch(f'{FILE}.len', return_value=tst_len)
        MatchCategory = namedtuple('MatchCategory',
                                   ['category', 'start_index', 'matches'])
        self.tst_matcher.match_categories = [MatchCategory(category='test_category',
                                                           start_index=tst_prev_index,
                                                           matches=None)]

        start_index = self.tst_matcher.get_start_index()

        assert start_index == exp_start_index

    @pytest.mark.parametrize("""repo_components, cluster_components,
                                expected_fm, expected_leftovers""",
                             [(tst_repo_components,
                               tst_cluster_components,
                               exp_full_matches,
                               exp_fm_leftovers)])
    def test_get_full_matches(self, repo_components, cluster_components,
                              expected_fm, expected_leftovers):
        """Test the get_full_matches method."""
        fm_results = self.tst_matcher.get_full_matches(cluster_components)

        fms = fm_results.full_matches
        leftovers = fm_results.leftovers

        for fmc, exp in zip_longest(fms, expected_fm):
            assert fmc.get_component().name == exp.name

        for lefto, exp_leftover in zip_longest(leftovers, expected_leftovers):
            assert lefto.name == exp_leftover.name

    @pytest.mark.parametrize("""repo_components, cluster_components,
                                expected_pm, expected_no_matches""",
                             [(tst_repo_components,
                               exp_fm_leftovers,
                               exp_partial_matches,
                               exp_pm_no_matches)])
    def test_get_partial_matches(self, repo_components, cluster_components,
                                 expected_pm, expected_no_matches):
        """Test the get_partial_matches method."""
        pm_results = self.tst_matcher.get_partial_matches(cluster_components)

        pms = pm_results.partial_matches
        no_matches = pm_results.no_matches

        for partial_match, exp in zip_longest(pms, expected_pm):
            assert partial_match.get_component().name == exp.name

        for no_match, exp_leftover in zip_longest(no_matches, expected_no_matches):
            assert no_match.name == exp_leftover.name

    @pytest.mark.parametrize("""repo_components, cluster_components,
                                expected_nm""",
                             [(tst_repo_components,
                               exp_pm_no_matches,
                               exp_no_matches)])
    def test_get_no_matches(self, repo_components, cluster_components,
                            expected_nm):
        """Test the get_no_matches method."""
        nm_results = self.tst_matcher.get_no_matches(cluster_components)

        for no_match, exp in zip(nm_results, expected_nm):
            assert no_match.get_component().name == exp.name
