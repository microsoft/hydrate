"""Hydrate generates a high level description of your cluster.

Functions:
    - main()
"""
import argparse
import os
from hydrate.cluster import Cluster
from hydrate.hld import Component, generate_HLD

curr_path = os.path.dirname(__file__)
tmp_path = os.path.relpath('tmp', curr_path)

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
        default=os.path.join(tmp_path, 'kubeconfig'),
        help='Kubeconfig file for the cluster (default:tmp/kubeconfig)',
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
    components = my_cluster.get_components()

    verbose_print("Creating Component object...")
    my_component = Component(args.name)

    verbose_print("Creating the list of subcomponents...")
    sub_list = []
    for each in components:
        s = Component(each[0])
        s.delete_none_attrs()
        sub_list.append(s)

    my_component.subcomponents = sub_list

    verbose_print("Writing component.yaml...")
    with open("component.yaml", "w") as of:
        generate_HLD(my_component, of)

