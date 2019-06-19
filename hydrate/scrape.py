"""Scrapes Github for Fabrikate Component Information."""

import urllib.parse
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

from .component import Component

# URL to the Fabrikate Component Definitions
GITHUB_URL = "https://github.com"
COMP_DEFS_URL = "https://github.com/microsoft/fabrikate-definitions/tree/master/definitions"


def get_repo_components():
    """Return the Fabrikate Component List."""
    response = simple_get(COMP_DEFS_URL)
    components = parse_html(response)
    components = remove_fabrikate_prefix(components)
    components = prepend_github_url(components)
    return components


def parse_html(html_bytes):
    """Parse the Components HTML, returning list of Components."""
    components = []
    soup = BeautifulSoup(html_bytes, features='html.parser')
    table = soup.find('table', attrs={'class': 'files'})
    for table_body in table.find_all('tbody'):
        for trs in table_body.find_all('tr',
                                       attrs={'class': 'js-navigation-item'}):
            for td in trs.find_all('td', attrs={'class': 'content'}):
                anchor = td.find('span').find('a')
                components.append(
                    Component(anchor['title'], source=anchor['href'])
                    )
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


def prepend_github_url(components):
    """Append the GitHub URL prefix to the component links."""
    for component in components:
        component.source = urllib.parse.urljoin(GITHUB_URL, component.source)
    return components


def simple_get(url):
    """Attempt to get the content at `url` by making an HTTP GET request.

    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """Return True if the response seems to be HTML, False otherwise."""
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def write_to_file(out_bytes, of):
    """Write to file."""
    with open(of, "wb") as f:
        f.write(out_bytes)
