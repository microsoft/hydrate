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

    def __eq__(self, other):
        """Override the default __eq__."""
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

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
            else:
                d = {key: value for key, value in self.__dict__.items()}
        except AttributeError:
            d = {key: value for key, value in self.__dict__.items()}
        return d

    def delete_none_attrs(self):
        """Remove attributes with value of None."""
        attr_dict = deepcopy(self.__dict__)

        for key, value in attr_dict.items():
            if value is None:
                delattr(self, key)


def get_full_matches(repo_components, cluster_components):
    """Return the Fabrikate Components that fully match the cluster."""
    full_matches = []
    cluster_set = set()
    for cc in cluster_components:
        cluster_set.add(cc.name)
    for rc in repo_components:
        repo_set = set(rc.name.split('-'))
        if repo_set <= cluster_set:
            # Full match. Every name for this component is in the cluster.
            cluster_set -= repo_set
            full_matches.append(rc)

    if cluster_set:
        print("Leftover deployments in cluster: {}".format(cluster_set))

    return full_matches
