"""Hydrate generates a high level description of your cluster.

Functions:
    - main()
"""
import argparse
import os
import sys
from hydrate.cluster import Cluster
from hydrate.hld import Component, generate_HLD

curr_path = os.path.dirname(__file__)
tmp_path = os.path.relpath('tmp', curr_path)


def main(args):
    """Generate the HLD for the cluster."""
    # Define verbose_print as print if -v, o.w. do nothing
    verbose_print = print if args.verbose else lambda *a, **k: None
    verbose_print("Printing verbosely...")

    print("Connecting to cluster...")
    my_cluster = Cluster(args.kubeconfig)
    my_cluster.connect_to_cluster()
    print("Connected!")

    print("Collecting information from the cluster...")
    components = my_cluster.get_components()

    verbose_print("Creating Component object...")
    my_component = Component(args.name)

    verbose_print("Creating the list of subcomponents...")
    sub_list = []
    for component in components:
        s = Component(component)
        s.delete_none_attrs()
        sub_list.append(s)

    my_component.subcomponents = sub_list

    print("Writing HLD...")

    if args.dry_run:
        verbose_print("Writing component.yaml to terminal...")
        generate_HLD(my_component, sys.stdout)
    else:
        if args.output:
            verbose_print("Writing component.yaml to {}.".format(args.output))
            output = os.path.join(args.output, "component.yaml")
            with open(output, "w") as of:
                generate_HLD(my_component, of)
        else:
            verbose_print("Writing to component.yaml...")
            with open("component.yaml", "w") as of:
                generate_HLD(my_component, of)


def parse_args():
    """Parse command line arguments."""
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
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args)
