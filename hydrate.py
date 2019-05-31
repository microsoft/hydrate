from kubernetes import client, config

def get_pods_for_all_namespaces():
    """Prints all the pods to the terminal.
    """
    v1 = client.CoreV1Api()
    print('Listing pods with their IPs:')
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

def get_deployments_for_all_namespaces():
    """Prints all the deployments and their conatiner images to the terminal.
    """
    api = client.AppsV1Api()
    print('Listing deployments:')
    print('Namespace\tName\tReplicas')
    ret = api.list_deployment_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.metadata.namespace, i.metadata.name, i.spec.replicas))
        print("\tImages:")
        for container in i.spec.template.spec.containers:
            print("\t%s" % (container.image))

if __name__ == '__main__':
    config.load_kube_config('kubeconfig')
    get_pods_for_all_namespaces()
    get_deployments_for_all_namespaces()
