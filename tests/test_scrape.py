"""Test suite for scrape.py."""
import pytest

from hydrate.component import Component
from hydrate.scrape import FAB_DEFS_URL, FAB_DEFS_API
from hydrate.scrape import get_repo_components
from hydrate.scrape import parse_json
from hydrate.scrape import construct_components
from hydrate.scrape import remove_fabrikate_prefix
from hydrate.scrape import json_get

@pytest.mark.parametrize('json_get_ret',
                         [(1), (None)])
def test_get_repo_components(mocker, json_get_ret):
    """Test the get_repo_components function."""
    mock_json_get = mocker.patch("hydrate.scrape.json_get",
                                 return_value=json_get_ret)
    mock_parse_json = mocker.patch("hydrate.scrape.parse_json",
                                   return_value=json_get_ret)
    mock_construct_components = mocker.patch(
        "hydrate.scrape.construct_components",
        return_value=json_get_ret)
    mock_rm_fab_prefix = mocker.patch("hydrate.scrape.remove_fabrikate_prefix")

    if json_get_ret:
        get_repo_components()
    else:
        with pytest.raises(Exception, match=r".* URL:%s" % (FAB_DEFS_API)):
            get_repo_components()

    mock_json_get.assert_called_once()

    if mock_json_get.return_value:
        mock_parse_json.assert_called_once()
        mock_construct_components.assert_called_once()
        mock_rm_fab_prefix.assert_called_once()
    else:
        mock_parse_json.assert_not_called()
        mock_construct_components.assert_not_called()
        mock_rm_fab_prefix.assert_not_called()


tst_json_list = [{"name": "Test1",
                  "source": FAB_DEFS_URL,
                  "html_url": "www.test1.com"},
                 {"name": "Test2",
                  "source": FAB_DEFS_URL,
                  "html_url": "www.test2.com"}]
exp_json_data = [{"name": "Test1",
                  "source": FAB_DEFS_URL,
                  "path": "www.test1.com"},
                 {"name": "Test2",
                  "source": FAB_DEFS_URL,
                  "path": "www.test2.com"}]

@pytest.mark.parametrize('json_list, exp_json_data',
                         [(tst_json_list, exp_json_data)])
def test_parse_json(json_list, exp_json_data):
    """Test parse_json function."""
    assert parse_json(json_list) == exp_json_data


exp_new_components = [Component(name="Test1",
                                source=FAB_DEFS_URL,
                                path="www.test1.com"),
                      Component(name="Test2",
                                source=FAB_DEFS_URL,
                                path="www.test2.com")]
@pytest.mark.parametrize('tst_json_data, exp_components',
                         [(exp_json_data, exp_new_components)])
def test_construct_components(tst_json_data, exp_components):
    """Test construct_components function."""
    assert construct_components(tst_json_data) == exp_components


tst_fab_comps = [Component(name="fabrikate-test-component"),
                 Component(name="fabrikate-test-component2"),
                 Component(name="test-component3")]
exp_no_fab_comps = [Component(name="test-component"),
                    Component(name="test-component2"),
                    Component(name="test-component3")]

@pytest.mark.parametrize('components, exp_components',
                         [(tst_fab_comps, exp_no_fab_comps)])
def test_remove_fabriakte_prefix(components, exp_components):
    """Test remove_fabriakte_prefix function."""
    assert remove_fabrikate_prefix(components) == exp_components


class Mock_Resp():
    """Mock the response object returned by requests.get()."""

    def __init__(self, status_code, json=None):
        """Initialize Mock_Resp object."""
        self.status_code = status_code
        self.json_obj = json

    def json(self):
        """Return json-like python object."""
        return self.json_obj


tst_url = "www.get-test-json.com"
exp_json = [{"test": "passed"}]
mock_resp_success = Mock_Resp(status_code=200, json=exp_json)
mock_resp_fail = Mock_Resp(status_code=404)


@pytest.mark.parametrize('tst_url, exp_json, mock_resp',
                         [(tst_url, exp_json, mock_resp_success),
                          (tst_url, None, mock_resp_fail)])
def test_json_get(mocker, tst_url, exp_json, mock_resp):
    """Test the json_get function."""
    mocker.patch('hydrate.scrape.get', return_value=mock_resp)
    assert json_get(tst_url) == exp_json
