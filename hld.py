"""Use to construct the HLD from given information."""
from ruamel.yaml import YAML
yaml = YAML()


class Component():
    """Hold the information for fabrikate High-Level Deployment(HLD)."""
    def __init__(self, name, generator="static", method="git"):
        """Instantiate a Component object.

        Args:
            name: string name of component
            generator: string type of manifest generation(default:static)
            method: string type of retrieval (default:git)

        """
        self._name = name
        self._generator = None
        self._source = None
        self._method = method
        self._path = None
        self._version = None
        self._branch = None
        self._hooks = None
        self._repositories = None
        self._subcomponents = None

    @property
    def name(self):
        return self._name

    @property
    def generator(self):
        return self._generator

    @property
    def source(self):
        return self._source

    @property
    def method(self):
        return self._method

    @property
    def path(self):
        return self._path

    @property
    def version(self):
        return self._version

    @property
    def branch(self):
        return self._branch

    @property
    def hooks(self):
        return self._hooks

    @property
    def repositories(self):
        return self._repositories

    @property
    def subcomponents(self):
        return self._subcomponents

    @name.setter
    def name(self, name):
        self._name = name

    @generator.setter
    def generator(self, generator):
        self._generator = generator

    @source.setter
    def source(self, source):
        self._source = source

    @method.setter
    def method(self, method):
        self._method = method

    @path.setter
    def path(self, path):
        self._path = path

    @version.setter
    def version(self, version):
        self._version = version

    @branch.setter
    def branch(self, branch):
        self._branch = branch

    @hooks.setter
    def hooks(self, hooks):
        self._hooks = hooks

    @repositories.setter
    def repositories(self, repositories):
        self._repositories = repositories

    @subcomponents.setter
    def subcomponents(self, subcomponents):
        self._subcomponents = subcomponents


def generate_HLD(component, output):
    """Create HLD yaml file.

    Args:
        component: Component object
        output: filestream

    """
    yaml.register_class(Component)
    yaml.dump(component, output)
