"""Fabrikate Component Class Definition."""

from copy import deepcopy


class Component():
    """Hold the information for fabrikate High-Level Deployment(HLD)."""

    def __init__(self, name, generator="static", 
                 source="<source repository url>", method="git",
                 path=None):
        """Instantiate a Component object.

        Args:
            name: string name of component
            generator: string type of manifest generation(default:static)
            method: string type of retrieval (default:git)

        """
        self.name = name
        self.generator = generator
        self.source = source
        self.method = method
        self.path = path
        self.version = None
        self.branch = None
        self.hooks = None
        self.repositories = None
        self.subcomponents = None

    def __str__(self):
        """Name of the Component."""
        return self.name

    # How the class is represented in yaml
    yaml_tag = u'Component'

    def asdict(self):
        """Return dict of Component."""
        d = dict()
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