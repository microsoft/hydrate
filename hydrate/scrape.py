"""Scrapes Github for Fabrikate Component Information."""
from requests import get

from .component import Component

# URL to the Fabrikate Component Definitions
COMP_DEFS_URL = "https://api.github.com/repos/microsoft/fabrikate-definitions/contents/definitions"


def get_repo_components():
    """Return the Fabrikate Component List."""
    json_string = json_get(COMP_DEFS_URL)
    components = parse_json(json_string)
    components = remove_fabrikate_prefix(components)
    for component in components:
        print(component)
    return components


def parse_json(json_list):
    """Parse json to get each component."""
    components = []
    for entry in json_list:
        component = Component(entry["name"], source=entry["html_url"])
        components.append(component)
    return components


def remove_fabrikate_prefix(components):
    """Remove the fabrikate prefix from the Component names."""
    fabrikate_found = False
    for component in components:
        words = component.name.split("-")
        new_title = ""
        if words[0] == "fabrikate":
            fabrikate_found = True
            words = words[1:]
        for idx, word in enumerate(words):
            if idx != 0:
                new_title += "-"
            new_title += word
        component.name = new_title
    if not fabrikate_found:
        print("Components do not contain Fabrikate prefix!")
    return components


def json_get(url):
    """Get the json at the url."""
    resp = get(url)
    if resp.status_code != 200:
        return None
    else:
        return resp.json()
