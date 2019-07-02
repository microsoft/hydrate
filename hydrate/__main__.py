"""Hydrate generates a high level description of your cluster.

Functions:
    - main()
"""
import argparse
import os
import sys
from pathlib import Path

from .cluster import Cluster
from .component import Component, match_components
from .hld import generate_HLD
from .scrape import get_repo_components


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
    cc = my_cluster.get_components()

    print("Collecting Fabrikate Components from GitHub...")
    rc = get_repo_components()

    print("Comparing Fabrikate Components to Cluster Deployments...")
    subcomponents, category_indeces = match_components(rc, cc)

    verbose_print("Creating Component object...")
    my_component = Component(args.name, path="./manifests")

    verbose_print("Creating the list of subcomponents...")
    sub_list = []
    for component in subcomponents:
        component.delete_none_attrs()
        sub_list.append(component)

    my_component.subcomponents = sub_list

    print("Writing HLD...")

    output_file = None
    if args.dry_run:
        verbose_print("Writing component.yaml to terminal...")
        generate_HLD(my_component, sys.stdout, category_indeces)

    else:
        if args.output:
            verbose_print("Writing component.yaml to {}.".format(args.output))
            output_file = os.path.join(args.output, "component.yaml")

        else:
            verbose_print("Writing to component.yaml...")
            output_file = "component.yaml"

        with open(output_file, "w") as of:
            generate_HLD(my_component, of, category_indeces)


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
        default=str(Path("tmp/kubeconfig").resolve()),
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
