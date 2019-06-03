"""Hydrate generates a high level description of your cluster.

Functions:
    - get_pods_for_all_namespaces()
    - get_deployments_for_all_namespaces()
"""
from kubernetes import client, config
import argparse
import os


def get_pods_for_all_namespaces():
    """Print all the pods to the terminal."""
    v1 = client.CoreV1Api()
    print('Listing pods with their IPs:')
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip,
                              i.metadata.namespace,
                              i.metadata.name))


def get_deployments_for_all_namespaces():
    """Print all the deployments and their conatiner images to the terminal."""
    api = client.AppsV1Api()
    print('Listing deployments:')
    print('Namespace\tName\tReplicas')
    ret = api.list_deployment_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.metadata.namespace,
                              i.metadata.name,
                              i.spec.replicas))
        print("\tImages:")
        for container in i.spec.template.spec.containers:
            print("\t%s" % (container.image))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate a component.yaml file for your cluster.')
    parser.add_argument(
        'run',
        help='Generate component.yaml for current configuration.')
    parser.add_argument(
        '-n', '--name',
        action='store',
        default='hydrated-cluster',
        help='Name of the main component (default:hydrated-cluster)')
    parser.add_argument(
        '-k', '--kubeconfig',
        action='store',
        default='kubeconfig',
        help='Kubeconfig file for the cluster (default:kubeconfig)',
        metavar='FILE')
    parser.add_argument(
        '-o', '--output',
        action='store',
        default=os.getcwd(),
        help='Output path for the generated component.yaml.',
        metavar='PATH')
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output logs.')
    parser.add_argument(
        '-d', '--dry-run',
        action='store_true',
        help='Print component.yaml to the terminal.')
    args = parser.parse_args()

    # Define verbose_print as print if -v, o.w. do nothing
    verbose_print = print if args.verbose else lambda *a, **k: None
    verbose_print("Printing verbosely...")

    config.load_kube_config('kubeconfig')
    get_pods_for_all_namespaces()
    get_deployments_for_all_namespaces()
