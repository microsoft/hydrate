"""Kubernetes Cluster API Class."""
from kubernetes import client, config


class Cluster():
    """Define Cluster data and methods."""

    def __init__(self, kubeconfig):
        """Instantiate Cluster object.

        Args:
            kubeconfig: credential file for cluster

        """
        self.kubeconfig = kubeconfig
        self.apps_v1_api = None
        self.core_v1_api = None
        self.connect_to_cluster()

    def connect_to_cluster(self):
        """Connect to the cluster. Set API attributes.
        """
        config.load_kube_config(self.kubeconfig)
        self.apps_v1_api = client.AppsV1Api()
        self.core_v1_api = client.CoreV1Api()

    def get_components(self):
        """Query the cluster for components.
        
        Returns:
            sorted dictionary of components in the cluster
        """
        pods = self.get_pods_for_all_namespaces()
        sorted_components = self.process_cluster_data(pods)
        return sorted_components

    def process_cluster_data(self, cluster_data):
        """Process cluster data for usage.
        
        Returns:
            dictionary of components
        """
        comp_list = count_first_word(cluster_data, "name")
        return sort_dict_by_value(comp_list)

    def get_pods_for_all_namespaces(self):
        """Return list of dicts of pod info.

        Returns:
            pod_list: list of dicts
        """
        pod_list = []
        ret = self.core_v1_api.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            d = dict()
            d["ip"] = i.status.pod_ip
            d["name"] = i.metadata.name
            d["namespace"] = i.metadata.namespace
            pod_list.append(d)

        return pod_list

    def get_deployments_for_all_namespaces(self):
        """Return list of dicts of deployment info.

        Returns:
            deployment_list: list of dicts

        """
        deployment_list = []
        ret = self.apps_v1_api.list_deployment_for_all_namespaces(watch=False)
        for i in ret.items:
            d = dict()
            d["name"] = i.metadata.name
            d["namespace"] = i.metadata.namespace
            d["replicas"] = i.spec.replicas

            container_list = []
            for container in i.spec.template.spec.containers:
                container_list.append(container.image)

            d["containers"] = container_list
            deployment_list.append(d)

        return deployment_list


def count_first_word(dict_list, key):
    """Count the first word of each dict[key] in the list.

    Args:
        dict_list: List of dictionaries
        key: Used to obtain the values from each dictionary

    Returns:
        dict(key:word, value:count) sorted by value desc. order

    """
    ret_count = dict()
    for item in dict_list:
        words = item[key].split("-")
        ret_count[words[0]] = ret_count.get(words[0], 0) + 1
    return ret_count

def sort_dict_by_value(d):
    """Sorts a dictionary by value.

    Args:
        d: Dictionary

    Returns:
        list: List of (key, value) sorted by value in descending order

    """
    return [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]