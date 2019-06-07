"""Hydrate generates a high level description of your cluster.

Functions:
    - main()
"""
import argparse
import os
from cluster import Cluster
from hld import Component, generate_HLD


def word_counts(dict_list, key):
    """Count the first word of each dict[key] in the list.

    Args:
        dict_list: List of dictionaries
        key: Used to obtain the values from each dictionary

    Returns:
        dict(key:word, value:count)

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

    # Connect to Cluster
    my_cluster = Cluster(args.kubeconfig)
    deployments = my_cluster.get_deployments_for_all_namespaces()
    pods = my_cluster.get_pods_for_all_namespaces()

    # Create Component
    my_component = Component(args.name)

    # Get first word counts
    dep_counts = word_counts(deployments, "name")
    pod_counts = word_counts(pods, "name")

    # Sort the word counts
    sorted_deps = sort_dict_by_value(dep_counts)
    sorted_pods = sort_dict_by_value(pod_counts)

    sub_list = []
    for each in sorted_pods:
        sub_list.append(Component(each[0]))

    my_component.subcomponents = sub_list

    with open("component.yaml", "w") as of:
        generate_HLD(my_component, of)
