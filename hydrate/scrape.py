from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


COMP_DEFS_URL = (
"https://github.com/microsoft/fabrikate-definitions/tree/master/definitions"
)


def parse_html(html_file):
    """Parses the Components HTML, returning urls"""
    titles = []
    raw_html = open(html_file).read()
    soup =  BeautifulSoup(raw_html, 'html.parser')
    table = soup.find('table', attrs={'class': 'files'})
    for table_body in table.find_all('tbody'):
        for trs in table_body.find_all('tr', attrs={'class': 'js-navigation-item'}):
            for td in trs.find_all('td', attrs={'class': 'content'}):
                titles.append(td.find('span').find('a')['title'])
    return titles


def remove_fabrikate_prefix(component_titles):
    """Removes the fabrikate prefix from the component titles."""
    ret_list = []
    for title in component_titles:
        words = title.split("-")
        new_title = ""
        if words[0] == "fabrikate":
            words = words[1:]
        for idx, word in enumerate(words):
            if idx != 0:
                new_title += "-"
            new_title += word
        ret_list.append(new_title)
    return ret_list


def get_fabrikate_components(output):
    """Writes the Fabrikate Component List HTML to the output file."""
    ret = simple_get(COMP_DEFS_URL)
    write_to_file(ret, output)


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content # pylint: disable=no-member
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def write_to_file(string, of):
    """Writes to file."""
    with open(of, "wb") as f:
        f.write(string)

