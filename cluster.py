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
        """Connect to the cluster. Set API attributes."""
        config.load_kube_config(self.kubeconfig)
        self.apps_v1_api = client.AppsV1Api()
        self.core_v1_api = client.CoreV1Api()

    def get_pods_for_all_namespaces(self):
        """Return list of dicts of pod info.

        Returns:
            pod_list: list of dicts

        """
        pod_list = []
        ret = self.core_v1_api.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            d = {}
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
            d = {}
            d["name"] = i.metadata.name
            d["namespace"] = i.metadata.namespace
            d["replicas"] = i.spec.replicas

            container_list = []
            for container in i.spec.template.spec.containers:
                container_list.append(container.image)

            d["containers"] = container_list
            deployment_list.append(d)

        return deployment_list
