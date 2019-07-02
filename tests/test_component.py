"""Test suite for component.py."""
import pytest
from itertools import zip_longest
from copy import deepcopy

from hydrate.component import Component, get_full_matches


class TestComponent():
    """Test Suite for Component Class."""

    tst_component = Component("Test")
    exp_component_asdict = {"name": tst_component.name,
                            "generator": tst_component.generator,
                            "source": tst_component.source,
                            "method": tst_component.method,
                            "path": tst_component.path,
                            "version": tst_component.version,
                            "branch": tst_component.branch,
                            "hooks": tst_component.hooks,
                            "repositories": tst_component.repositories,
                            "subcomponents": tst_component.subcomponents
                            }

    tst_component_none_attrs = Component("NoneAttrs")

    exp_component_none_attrs = Component("NoneAttrs")
    attr_dict = deepcopy(exp_component_none_attrs.__dict__)
    for key, value in attr_dict.items():
        if value is None:
            delattr(exp_component_none_attrs, key)

    def test_asdict(self):
        """Test the asdict() method."""
        assert self.tst_component.asdict() == self.exp_component_asdict

    def test_delete_none_attrs(self):
        """Test the delete_none_attrs method."""
        self.tst_component_none_attrs.delete_none_attrs()
        assert self.tst_component_none_attrs == self.exp_component_none_attrs


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
exp_leftovers = [Component("dep4"),
                 Component("dep6")]


@pytest.mark.parametrize('''repo_components, cluster_components,
                            expected_fm, expected_leftos''',
                         [(tst_repo_components,
                           tst_cluster_components,
                           exp_full_matches,
                           exp_leftovers)])
def test_get_full_matches(repo_components, cluster_components,
                          expected_fm, expected_leftos):
    """Test get_full_matches()."""
    fms, leftos = get_full_matches(repo_components, cluster_components)

    for fmc, exp in zip_longest(fms, exp_full_matches):
        assert fmc.name == exp.name

    for lefto, exp_lefto in zip_longest(leftos, exp_leftovers):
        assert lefto.name == exp_lefto.name
