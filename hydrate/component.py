"""Fabrikate Component Class Definition."""

from copy import deepcopy


class Component():
    """Hold the information for fabrikate High-Level Deployment(HLD)."""

    def __init__(self, name, generator=None, source="<source repository url>",
                 method="git", path=None, version=None, branch=None,
                 hooks=None, repositories=None, subcomponents=None):
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
        self.version = version
        self.branch = branch
        self.hooks = hooks
        self.repositories = repositories
        self.subcomponents = subcomponents

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


NO_MATCH_STR = '''No Match Deployments
In order to use these deployments with Fabrikate, follow the steps below.
1. Populate the source (git repository link)
2. Add a path field (path within the git repository) ex: "path: stable/"
3. Specify helm for applications generated using a Helm chart ex: "type: helm"
Otherwise, comment them out to prevent errors with Fabrikate generation.'''


def match_components(repo_components, cluster_components):
    """Match cluster and repo components."""
    subcomponents = []
    category_indeces = []
    rc = repo_components
    cc = cluster_components
    full_matches, fm_leftovers = get_full_matches(rc, cc)

    # Indeces are determined by the length of the previous category
    if full_matches:
        subcomponents.extend(full_matches)
        category_indeces.append((0, "Full Match Components"))

    if fm_leftovers:
        subcomponents.extend(fm_leftovers)
        category_indeces.append((len(full_matches), NO_MATCH_STR))

    return subcomponents, category_indeces


def get_full_matches(repo_components, cluster_components):
    """Determine which components fully match the cluster.

    Returns:
        full_matches: list of components
        leftovers: list of components

    """
    full_matches = []
    cluster_set = set()
    leftovers = None
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
        leftovers = [cc for cc in cluster_components if cc.name in cluster_set]

    return full_matches, leftovers
