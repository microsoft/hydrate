"""Test suite for component.py."""

from copy import deepcopy

from hydrate.component import Component
from hydrate.component import TopComponent


class TestComponent():
    """Test Suite for Component Class."""

    tst_component = Component(name="Test")
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

    tst_component_none_attrs = Component(name="NoneAttrs")

    exp_component_none_attrs = Component(name="NoneAttrs")
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

    def test_delete_non_default_attributes(self):
        """Test the delete_non_default_attributes method."""
        tst_component = Component(name="test-component")
        tst_component.x = "Should be removed"

        tst_component.delete_non_default_attributes()

        assert not hasattr(tst_component, 'x')


def test_TopComponent():
    """Test the TopComponent class."""
    tst_top_component = TopComponent(name="test-TopComponent")

    assert tst_top_component.generator == 'static'
    assert tst_top_component.source is None
    assert tst_top_component.method is None
    assert tst_top_component.path == './manifests'
