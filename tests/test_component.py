"""Test suite for component.py."""
import pytest
from itertools import zip_longest
from hydrate.component import Component, get_full_matches


tst_cluster_components = [Component("dep1"),
                          Component("dep2"),
                          Component("dep3"),
                          Component("dep4"),
                          Component("dep6")]
tst_repo_components = [Component("dep1-dep2"),
                       Component("dep3"),
                       Component("dep4-dep5")]
exp_full_matches = [Component("dep1-dep2"),
                    Component("dep3")]


@pytest.mark.parametrize('repo_components, cluster_components, expected',
                         [(tst_repo_components,
                           tst_cluster_components,
                           exp_full_matches)])
def test_get_full_matches(repo_components, cluster_components, expected):
    """Test get_full_matches()."""
    full_matches = get_full_matches(repo_components, cluster_components)
    for index, (fmc, exp) in enumerate(zip_longest(full_matches,
                                                   exp_full_matches)):
        assert fmc.name == exp.name
