from kubernetes import client, config

def connect_to_cluster():
    """Connects to the cluster defined in the kubeconfig file, and prints the pods.
    """
    config.load_kube_config("kubeconfig")
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

if __name__ == "__main__":
    connect_to_cluster()
