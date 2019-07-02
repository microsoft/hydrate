"""Scrapes Github for Fabrikate Component Information."""
from requests import get
import re

from .component import Component

# URL to the Fabrikate Component Definitions
FAB_DEFS_URL = "https://github.com/microsoft/fabrikate-definitions"
FAB_DEFS_API = "https://api.github.com/repos/microsoft/fabrikate-definitions/contents/definitions"


def get_repo_components():
    """Return the Fabrikate Component List."""
    json_obj = json_get(FAB_DEFS_API)
    if json_obj:
        json_data = parse_json(json_obj)
        components = construct_components(json_data)
        components = remove_fabrikate_prefix(components)
        return components
    raise Exception('JSON not retrieved. URL:{}'.format(FAB_DEFS_API))


def get_path(html_url):
    """Get the component path from the html_url."""
    return re.sub(r'.*master/', '', html_url)


def construct_components(json_data):
    """Construct Component objects using a list of data tuples."""
    components = []
    for defintion in json_data:
        components.append(
            Component(name=defintion["name"],
                      source=defintion["source"],
                      path=defintion["path"]))
    return components


def parse_json(json_list):
    """Parse json to get information for each definition.

    Returns:
        dict

    """
    json_dicts = []
    for entry in json_list:
        json_data = {
                     'name': entry["name"],
                     'source': FAB_DEFS_URL,
                     'path': get_path(entry["html_url"])
                    }
        json_dicts.append(json_data)
    return json_dicts


def remove_fabrikate_prefix(components):
    """Remove the fabrikate prefix from the Component names."""
    for component in components:
        component.name = re.sub('^fabrikate-', '', component.name)
    return components


def json_get(url):
    """Get the json at the url."""
    resp = get(url)
    if resp.status_code != 200:
        return None
    return resp.json()
