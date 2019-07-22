"""Fabrikate Component Class Definition."""

from copy import deepcopy


class Component():
    """Hold the information for fabrikate High-Level Deployment(HLD)."""

    def __init__(self, component=None, name='hydrated-component', generator=None,
                 source='<source repository url>', method='git', path=None,
                 version=None, branch=None, hooks=None, repositories=None,
                 subcomponents=None):
        """Instantiate a Component object.

        Args:
            component: Component object to make a copy of
            name: string name of component(default:hydrated-component)
            generator: string type of manifest generation(default:None)
            source: string url to repository(default:<source repository url>)
            method: string type of retrieval (default:git)
            path: string path in repository to component
            version: string commit hash representing

        """
        if isinstance(component, Component):
            self.__dict__ = {**self.__dict__, **deepcopy(component.__dict__)}
        else:
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

    def as_yaml(self):
        """Return dict of Component suitable for dumping to yaml."""
        self.delete_non_default_attributes()
        self.delete_none_attrs()
        return self.asdict()

    def asdict(self):
        """Return dict of Component."""
        d = dict()
        try:
            if self.subcomponents:
                d = {key: value for key, value in self.__dict__.items()
                     if key != 'subcomponents'}
                d['subcomponents'] = []
                for subcomponent in self.subcomponents:
                    d['subcomponents'].append(subcomponent.asdict())
            else:
                d = {key: value for key, value in self.__dict__.items()}
        except AttributeError:
            d = {key: value for key, value in self.__dict__.items()}
        return d

    def delete_non_default_attributes(self):
        """Remove non-default attributes from the instance."""
        DEFAULT_ATTRIBUTES = {'name', 'generator', 'source', 'method', 'path', 'version',
                              'branch', 'hooks', 'repositories', 'subcomponents'}
        attr_dict = deepcopy(self.__dict__)

        for key in attr_dict:
            if key not in DEFAULT_ATTRIBUTES:
                delattr(self, key)

    def delete_none_attrs(self):
        """Remove attributes with value of None."""
        attr_dict = deepcopy(self.__dict__)

        for key, value in attr_dict.items():
            if value is None:
                delattr(self, key)


class TopComponent(Component):
    """Top Level Component subclass."""

    def __init__(self, **kwargs):
        """Instantiate a TopComponent object."""
        Component.__init__(self,
                           generator='static',
                           source=None,
                           method=None,
                           path='./manifests',
                           **kwargs)


class CommentedComponent(Component):
    """Component with inline comment string."""

    def __init__(self, inline_comment, **kwargs):
        """Instantiate a CommentedComponent object."""
        self.inline_comment = inline_comment
        Component.__init__(self, **kwargs)
