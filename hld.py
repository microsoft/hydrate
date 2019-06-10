"""Use to construct the HLD from given information."""
from copy import deepcopy
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
        self.name = name
        self.generator = generator
        self.source = None
        self.method = method
        self.path = None
        self.version = None
        self.branch = None
        self.hooks = None
        self.repositories = None
        self.subcomponents = None

    # How the class is represented in yaml
    yaml_tag = u'Component'

    def asdict(self):
        """Return dict of Component."""
        d = {}
        try:
            if self.subcomponents:
                d = {key: value for key, value in self.__dict__.items()
                     if key != "subcomponents"}
                d["subcomponents"] = []
                for subcomponent in self.subcomponents:
                    d["subcomponents"].append(subcomponent.asdict())

        except AttributeError:
            d = {key: value for key, value in self.__dict__.items()}
        return d

    def delete_none_attrs(self):
        """Remove attributes with value of None."""
        attr_dict = deepcopy(self.__dict__)

        for key, value in attr_dict.items():
            if value is None:
                delattr(self, key)

    def prep(self):
        """Prep the object for yaml output."""
        pass


def generate_HLD(component, output):
    """Create HLD yaml file.

    Args:
        component: Component object
        output: filestream

    """
    component.delete_none_attrs()
    yaml.indent(mapping=2, sequence=4, offset=2)
    d = component.asdict()

    yaml.dump(d, output)
