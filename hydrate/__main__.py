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
from timeit import default_timer

from .hld import HLD_Generator
from .telemetry import Telemetry


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
        default='',
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
    parser.add_argument(
        '-t', '--telemetry',
        action='store_true',
        default=False,
        help='Enable telemetry data collection.')

    return parser.parse_args(args)


def main():
    """Generate the HLD for the cluster."""
    args = parse_args(sys.argv[1:])

    # Enable/Disable telemetry based on argument. Default: Disabled
    telemetry = Telemetry(args.telemetry)

    start_time = default_timer()

    # Generates HLD and manifests directory.
    hydrator = HLD_Generator(args)
    hydrator.generate()

    runtime = default_timer() - start_time

    telemetry.track_event("Hydrate executed")
    telemetry.track_metric("Hydrate runtime", runtime)
    print(f"Hydrate runtime: {runtime}")
    telemetry.flush()


if __name__ == '__main__':
    main()
