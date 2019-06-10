"""Hydrate generates a high level description of your cluster.

Functions:
    - main()
"""
import argparse
import os
from cluster import Cluster
from hld import Component, generate_HLD


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
    return sort_dict_by_value(ret_count)


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

    verbose_print("Connecting to cluster...")
    my_cluster = Cluster(args.kubeconfig)
    verbose_print("Connected!")

    verbose_print("Collecting information from the cluster...")
    deployments = my_cluster.get_deployments_for_all_namespaces()
    pods = my_cluster.get_pods_for_all_namespaces()

    verbose_print("Creating Component object...")
    my_component = Component(args.name)

    verbose_print("Getting first word counts...")
    dep_counts = count_first_word(deployments, "name")
    pod_counts = count_first_word(pods, "name")

    verbose_print("Creating the list of subcomponents...")
    verbose_print("Deleting None attributes from subcomponents...")
    sub_list = []
    for each in pod_counts:
        s = Component(each[0])
        s.delete_none_attrs()
        sub_list.append(s)

    my_component.subcomponents = sub_list

    verbose_print("Writing component.yaml...")
    with open("component.yaml", "w") as of:
        generate_HLD(my_component, of)
