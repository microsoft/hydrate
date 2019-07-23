"""Create manifest directory and populate it."""

import os
from ruamel.yaml import YAML

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


def generate_manifests(namespaces=None, directory="manifests"):
    """Make and populate manifests directory.

    Creates the manifests directory if it doesn't already exist, and populates
    it with the following yaml files:
        - namespaces.yaml

    Args:
        namespaces: list of strings (default: None)
        directory: string path (default:'manifests')

    """
    _make_directory(directory)

    if namespaces:
        namespaces_file = os.path.join(directory, "namespaces.yaml")
        data = _create_namespaces_data(namespaces)
        with open(namespaces_file, 'w') as of:
            _generate_namespaces_yaml(data, of)


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
