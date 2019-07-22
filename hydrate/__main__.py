"""Hydrate generates a high level description of your cluster.

GitHub Repo: https://github.com/microsoft/hydrate

Functions:
    - main()
    - parse_args()
"""
import os
import sys
from argparse import ArgumentParser
from pathlib import Path

from .hld import HLD_Generator


def main(args):
    """Generate the HLD for the cluster."""
    hydrator = HLD_Generator(args)
    hydrator.generate()


def parse_args(args):
    """Parse command line arguments."""
    parser = ArgumentParser(
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

    return parser.parse_args(args)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    main(args)
