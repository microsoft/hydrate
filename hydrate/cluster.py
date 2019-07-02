"""Kubernetes Cluster API Class."""
from kubernetes import client, config
from .component import Component
import re


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
        self.namespaced_pods = dict()
        self.namespaced_deployments = dict()

    def connect_to_cluster(self):
        """Connect to the cluster. Set API attributes."""
        config.load_kube_config(self.kubeconfig)
        self.apps_v1_api = client.AppsV1Api()
        self.core_v1_api = client.CoreV1Api()

    def get_components(self):
        """Query the cluster for components.

        Returns:
            sorted dictionary of components in the cluster

        """
        components = []
        default_deps = self.get_namespaced_deployments("default")
        namespaces = self.get_namespaces()
        namespaces = self.remove_defaults(namespaces)
        # Scenario where cluster applications live in namespaces
        if namespaces:
            first_words = [get_first_word(name) for name in namespaces]
            components.extend([Component(word) for word in first_words])
        # Scenario where cluster applications live in default
        if default_deps:
            dep_names = [
                re.sub(r'-deployment', '', dep) for dep in default_deps]
            components.extend([Component(n) for n in dep_names])

        return components

    def get_statefulsets(self):
        """Query the cluster for statefulsets."""
        ret = self.apps_v1_api.list_stateful_set_for_all_namespaces()
        with open("statefulsets.json", "w") as of:
            of.write(dict(ret))

    def get_namespaces(self):
        """Query the cluster for namespaces."""
        ret = self.core_v1_api.list_namespace()
        return [i.metadata.name for i in ret.items]

    def get_namespaced_deployments(self, namespace):
        """Store the list of deployments in the namespace.

        Args:
            namespace: The namespace to look in.

        Return:
            deployment_list: list of pods found in the namespace.
        """
        if namespace in self.namespaced_deployments:
            return self.namespaced_deployments[namespace]
        else:
            ret = self.apps_v1_api.list_namespaced_deployment(namespace)
            deployment_list = [i.metadata.name for i in ret.items]
            self.namespaced_pods[namespace] = deployment_list
            return deployment_list

    def get_namespaced_pods(self, namespace):
        """Store the list of pods in the namespace.

        Args:
            namespace: The namespace to look in.

        Return:
            pod_list: list of pods found in the namespace.
        """
        if namespace in self.namespaced_pods:
            return self.namespaced_pods[namespace]
        else:
            ret = self.core_v1_api.list_namespaced_pod(namespace)
            pod_list = [i.metadata.name for i in ret.items]
            self.namespaced_pods[namespace] = pod_list
            return pod_list

    def process_cluster_objects(self, object_list):
        """Process a list of kubernetes objects.

        Args:
            object_list: list of object names

        Returns:
            comp_list: component names sorted by value in desc. order

        """
        comp_list = count_first_word(object_list)
        comp_list = sort_dict_by_value(comp_list)
        # Take just the component name, not the frequency
        comp_list = [Component(component[0]) for component in comp_list]
        return comp_list

    def remove_defaults(self, namespaces):
        """Remove the default and kubernetes namespaces.

        Returns:
            ret_list: list of namespaces

        """
        ret_list = []
        ignore_set = {"default", "kube-public", "kube-system"}
        for namespace in namespaces:
            if namespace not in ignore_set:
                ret_list.append(namespace)
        return ret_list


def get_first_word(string, delimiter="-"):
    """Return the first word of a string, split by a delimiter.

    Args:
        string: string input
        delimiter: separator between words (default:"-")

    Returns:
        words[0]: first word of input string

    """
    words = string.split(delimiter)
    return words[0]


def count_first_word(str_list):
    """Count the first word of each string in the list.

    Args:
        str_list: List of strings

    Returns:
        {"word": count, ...}

    """
    ret_count = dict()
    for phrase in str_list:
        words = phrase.split("-")
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
