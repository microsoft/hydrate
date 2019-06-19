"""Use to construct the High-Level Deployment."""
from ruamel.yaml import YAML
yaml = YAML()


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
