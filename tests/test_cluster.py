"""Test suite for cluster.py."""
import pytest

from hydrate.component import Component
from hydrate.cluster import Cluster
from hydrate.cluster import get_first_word
from hydrate.cluster import count_first_word
from hydrate.cluster import sort_dict_by_value


class TestCluster():
    """Test suite for the Cluster class."""

    @pytest.fixture
    def cluster_connection(self, mocker):
        """Reusable cluster_connection object."""
        mock_cluster = Cluster("tst-kubeconfig")
        mock_cluster.apps_v1_api = mocker.Mock()
        mock_cluster.core_v1_api = mocker.Mock()
        return mock_cluster

    @pytest.fixture
    def metadata_items(self, mocker):
        """Mock a list of items with metadata.name attributes."""
        def _items(tst_input):
            meta_items = []
            for item in tst_input:
                mock_metadata_item = mocker.Mock()
                mock_metadata_item.metadata.name = item
                meta_items.append(mock_metadata_item)
            return meta_items
        return _items

    def test_connect_to_cluster(self, mocker, cluster_connection):
        """Test the method connect_to_cluster."""
        mock_config = mocker.patch("hydrate.cluster.config", autospec=True)
        mock_client = mocker.patch("hydrate.cluster.client", autospec=True)

        cluster_connection.connect_to_cluster()

        mock_config.load_kube_config.assert_called_once()
        mock_client.AppsV1Api.assert_called_once()
        mock_client.CoreV1Api.assert_called_once()

    tst_namespaces = ["elasticsearch", "istio", "jaeger"]
    tst_pods = ["elasticsearch-pod", "istio-pod", "jaeger-pod"]

    @pytest.mark.parametrize("tst_namespaces, tst_pods",
                             [(tst_namespaces, None),
                              (None, tst_pods)])
    def test_get_components(self, mocker, cluster_connection,
                            tst_namespaces, tst_pods):
        """Test the method get_components."""
        mock_get_namespaces = mocker.patch(
            "hydrate.cluster.Cluster.get_namespaces",
            return_value=tst_namespaces)
        mock_remove_defaults = mocker.patch(
            "hydrate.cluster.Cluster.remove_defaults",
            return_value=tst_namespaces)
        mock_get_first_word = mocker.patch("hydrate.cluster.get_first_word")
        mock_get_namespaced_pods = mocker.patch(
            "hydrate.cluster.Cluster.get_namespaced_pods",
            return_value=tst_pods)
        mock_process_cluster_objects = mocker.patch(
            "hydrate.cluster.Cluster.process_cluster_objects",
            return_value=tst_pods)

        components = cluster_connection.get_components()

        assert components
        mock_get_namespaces.assert_called_once()
        mock_remove_defaults.assert_called_once()
        if tst_namespaces:
            mock_get_first_word.assert_called()
        else:
            mock_get_namespaced_pods.assert_called_once()
            mock_process_cluster_objects.assert_called_once()

    tst_get_namespaces = ["elasticsearch", "istio", "jaeger"]
    @pytest.mark.parametrize("tst_get_namespaces",
                             [(tst_get_namespaces)])
    def test_get_namespaces(self, mocker, cluster_connection, metadata_items,
                            tst_get_namespaces):
        """Test Cluster.get_namespaces function."""
        mock_return_obj = mocker.Mock()
        mock_return_obj.items = metadata_items(tst_get_namespaces)
        mock_cluster = cluster_connection
        mock_cluster.core_v1_api.list_namespace.return_value = mock_return_obj

        namespaces = mock_cluster.get_namespaces()

        assert namespaces == tst_get_namespaces

    tst_get_namespaced_pods = ["elasticsearch-pod", "istio-pod"]
    @pytest.mark.parametrize("tst_pods", [(tst_get_namespaced_pods)])
    def test_get_namespaced_pods(self, mocker, cluster_connection,
                                 metadata_items, tst_pods):
        """Test Cluster.get_namespaced_pods function."""
        mock_return_obj = mocker.Mock()
        mock_return_obj.items = metadata_items(tst_pods)
        mock_cluster = cluster_connection
        mock_cluster.core_v1_api.list_namespaced_pod.return_value = \
            mock_return_obj

        pods = mock_cluster.get_namespaced_pods("FizzBuzz")

        assert pods == tst_pods

    tst_process_cluster_objects = [("elasticsearch", 1), ("istio", 1),
                                   ("jaeger", 1)]
    exp_process_cluster_objects = [Component("elasticsearch"),
                                   Component("istio"),
                                   Component("jaeger")]

    @pytest.mark.parametrize("tst_objects, exp_components",
                             [(tst_process_cluster_objects,
                               exp_process_cluster_objects)])
    def test_process_cluster_objects(self, mocker, cluster_connection,
                                     tst_objects, exp_components):
        """Test Cluster.process_cluster_objects function."""
        mock_count_first_word = mocker.patch(
            "hydrate.cluster.count_first_word",
            return_value=tst_objects)
        mock_sort_dict_by_value = mocker.patch(
            "hydrate.cluster.sort_dict_by_value",
            return_value=tst_objects)

        components = cluster_connection.process_cluster_objects(tst_objects)

        for cc, ec in zip(components, exp_components):
            assert cc.name == ec.name
        mock_count_first_word.assert_called_once()
        mock_sort_dict_by_value.assert_called_once()

    tst_remove_defaults1 = ["default", "kube-public", "kube-system"]
    exp_remove_defaults1 = []
    tst_remove_defaults2 = ["default", "elasticsearch"]
    exp_remove_defaults2 = ["elasticsearch"]

    @pytest.mark.parametrize("tst_namespaces, exp_namespaces",
                             [(tst_remove_defaults1, exp_remove_defaults1),
                              (tst_remove_defaults2, exp_remove_defaults2)])
    def test_remove_defaults(self, cluster_connection,
                             tst_namespaces, exp_namespaces):
        """Test Cluster.remove_defaults function."""
        mock_cluster = cluster_connection
        assert mock_cluster.remove_defaults(tst_namespaces) == exp_namespaces


tst_string = "fabrikate-elasticsearch"
exp_string = "fabrikate"

@pytest.mark.parametrize('string, delimiter, expected',
                         [(tst_string, "-", exp_string)])
def test_get_first_word(string, delimiter, expected):
    """Test get_first_word function."""
    assert get_first_word(string, delimiter) == expected


tst_str_list = ["apple", "apple", "orange", "apple", "banana", "orange"]
exp_str_list = {"apple": 3, "orange": 2, "banana": 1}

@pytest.mark.parametrize('str_list, expected',
                         [(tst_str_list, exp_str_list)])
def test_count_first_word(str_list, expected):
    """Test count_first_word function."""
    assert count_first_word(str_list) == expected


tst_fruits = {"apple": 1, "banana": 2, "orange": 3, "kiwi": 4,
              "mango": 5, "raspberry": 6, "peach": 7}
exp_fruits = [('peach', 7), ('raspberry', 6), ('mango', 5),
              ('kiwi', 4), ('orange', 3), ('banana', 2),
              ('apple', 1)]

@pytest.mark.parametrize('d, expected',
                         [(tst_fruits, exp_fruits)])
def test_sort_dict_by_value(d, expected):
    """Test sort_dict_by_value function."""
    assert sort_dict_by_value(d) == expected
