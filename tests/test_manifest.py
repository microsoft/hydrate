"""Test the manifest.py file."""
from io import StringIO
import pytest

from hydrate.manifest import NamespaceYAML
from hydrate.manifest import generate_manifests
from hydrate.manifest import _make_directory
from hydrate.manifest import _create_namespaces_data
from hydrate.manifest import _generate_namespaces_yaml


def test_NamespaceYAML():
    """Test the NamespaceYAML class."""
    tst_data = NamespaceYAML("Test Namespace")
    assert tst_data.apiVersion == "v1"
    assert tst_data.kind == "Namespace"
    assert tst_data.metadata["name"] == "Test Namespace"

tst_dry_run = [True, False]
@pytest.mark.parametrize('dry_run', tst_dry_run)
def test_generate_manifests(mocker, dry_run):
    """Test the generate_manifests function."""
    tst_namespaces = ["test1", "test2", "test3"]
    mock_make_directory = mocker.patch("hydrate.manifest._make_directory")
    mock_create_namespaces_data = mocker.patch(
        "hydrate.manifest._create_namespaces_data")
    mock_generate_namespaces_yaml = mocker.patch(
        "hydrate.manifest._generate_namespaces_yaml")
    mock_ospath_join = mocker.patch(
        "hydrate.manifest.os.path.join")

    generate_manifests(namespaces=tst_namespaces, dry_run=dry_run)

    mock_create_namespaces_data.assert_called_with(tst_namespaces)
    mock_generate_namespaces_yaml.assert_called_once()
    if not dry_run:
        mock_make_directory.assert_called_with("manifests")
        mock_ospath_join.assert_called_once()



def test_make_directory(mocker):
    """Test the _make_directory function."""
    mock_os_makedirs = mocker.patch("hydrate.manifest.os.makedirs")
    tst_path = "tst-manifests"

    _make_directory(tst_path)

    mock_os_makedirs.assert_called_with(tst_path, exist_ok=True)


def test_create_namespaces_data():
    """Test the _create_namespaces_data function."""
    tst_data = ["test1", "test2", "test3"]
    exp_return = [NamespaceYAML("test1"),
                  NamespaceYAML("test2"),
                  NamespaceYAML("test3")]

    tst_return = _create_namespaces_data(tst_data)

    for tst_obj, exp_obj in zip(tst_return, exp_return):
        assert tst_obj == exp_obj


def test_generate_namespaces_yaml():
    """Test the _generate_namespaces_yaml function."""
    tst_data = [NamespaceYAML("test1"),
                NamespaceYAML("test2"),
                NamespaceYAML("test3")]
    tst_outfile = StringIO()
    exp_outfile = """apiVersion: v1
kind: Namespace
metadata:
  name: test1
---
apiVersion: v1
kind: Namespace
metadata:
  name: test2
---
apiVersion: v1
kind: Namespace
metadata:
  name: test3
"""

    _generate_namespaces_yaml(tst_data, tst_outfile)

    tst_outfile.seek(0)
    assert tst_outfile.read() == exp_outfile
