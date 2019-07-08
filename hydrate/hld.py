"""Use to construct the High-Level Deployment."""
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml import YAML
yaml = YAML()

OFFSET = 2

TOP_LVL_COMMENT = '''Automatically generated using hydrate.
Repository link: https://github.com/microsoft/hydrate
Fabrikate Docs: https://github.com/Microsoft/fabrikate
For private repositories, check the following:
Authentication: https://github.com/microsoft/fabrikate/blob/master/docs/auth.md
For more information on how components are structured, check the following:
Component Model: https://github.com/microsoft/fabrikate/blob/master/docs/component.md''' # noqa


def generate_HLD(component, output, comment_indeces=None):
    """Create HLD yaml file.

    Args:
        component: Component object
        output: filestream
        comment_indeces: List of tuples (index, comment text)

    """
    component.delete_none_attrs()
    yaml.indent(mapping=2, sequence=4, offset=OFFSET)
    d = component.asdict()
    if comment_indeces:
        d = CommentedMap(d)
        d.yaml_set_start_comment(TOP_LVL_COMMENT)
        lst = CommentedSeq(d["subcomponents"])
        for idx, comment in comment_indeces:
            lst.yaml_set_comment_before_after_key(idx, comment, OFFSET)
        d["subcomponents"] = lst

    yaml.dump(d, output)
