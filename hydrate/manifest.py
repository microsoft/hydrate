"""Create manifest directory and populate it."""

import os
from io import StringIO
from ruamel.yaml import YAML
from .cluster import remove_default_namespaces

MAPPING = 2
SEQUENCE = 4
OFFSET = 2


class NamespaceYAML:
    """Structure of namespace.yaml entries."""

    def __init__(self, namespace):
        """Instantiate NamespaceYAML object."""
        self.apiVersion = "v1"
        self.kind = "Namespace"
        self.metadata = {"name": namespace}

    def __eq__(self, other):
        """Define equals operator between NamespaceYAML objects."""
        if not isinstance(other, NamespaceYAML):
            return NotImplemented

        return (self.apiVersion == other.apiVersion and
                self.kind == other.kind and
                self.metadata == other.metadata)


def generate_manifests(namespaces=None, directory="manifests", dry_run=False):
    """Make and populate manifests directory.

    Creates the manifests directory if it doesn't already exist, and populates
    it with the following yaml files:
        - namespaces.yaml

    Args:
        namespaces: list of strings (default: None)
        directory: string path (default:'manifests')

    """
    if namespaces:
        namespaces = remove_default_namespaces(namespaces)
        data = _create_namespaces_data(namespaces)
        if not dry_run:
            _make_directory(directory)
            namespaces_file = os.path.join(directory, "namespaces.yaml")
            with open(namespaces_file, 'w') as of:
                _generate_namespaces_yaml(data, of)
        else:
            print("Dry Run: namespaces.yaml:")
            of = StringIO()
            _generate_namespaces_yaml(data, of)
            of.seek(0)
            print(of.read())

    else:
        raise Exception("Namespaces are None")


def _make_directory(path):
    """Make directory, or do nothing if it already exists.

    Args:
        path: string

    """
    os.makedirs(path, exist_ok=True)


def _create_namespaces_data(namespaces):
    """Structure namespaces into namespace.yaml data.

    Args:
        namespaces: list of namespace strings

    """
    return [NamespaceYAML(namespace) for namespace in namespaces]


def _generate_namespaces_yaml(namespace_yamls, outfile):
    """Generate namespaces.yaml file from namespace_yamls data.

    Args:
        namespace_yamls: list of NamespaceYAML objects

    """
    yaml = YAML()
    yaml.explicit_start = False
    yaml.indent(mapping=MAPPING, sequence=SEQUENCE, offset=OFFSET)
    for idx, namespace in enumerate(namespace_yamls):
        if idx != 0 and not yaml.explicit_start:
            yaml.explicit_start = True
        yaml.dump(vars(namespace), outfile)
