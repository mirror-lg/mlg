"""
Execute library commands from cli
"""

import argparse
import getpass
import json
import logging
from typing import Generic, Dict
from argparse import Namespace

from mirror_lg.lib.shared import validate_prefix
from mirror_lg.lib.ios.ios_lib import IosLib




def _execute_cli() -> None:
    """
    cli args and options
    """

    parser = argparse.ArgumentParser(description='mirror looking glass cli')
    parser.add_argument('--username',
                        type=str,
                        help='username for connecting to the target router',
                        required=True)
    parser.add_argument('--target',
                        type=str,
                        help="IP or FQDN of the target router",
                        required=True)

    parser.add_argument('--prefix',
                        type=str,
                        help="Destination prefix for route table lookup",
                        required=True)

    subparsers = parser.add_subparsers(title='NOS specific commands',
                                       description='specific network OS '
                                                   'commands')

    ios_cli_parser = subparsers.add_parser('ios_cli',
                                           help='Run commands on legacy Cisco '
                                                'ios devices')

    ios_cli_parser.set_defaults(func=ios_cli)
    ios_cli_parser.add_argument('--route-lookup',
                                action='store_true',
                                help='route table lookup',
                                default=False)
    ios_cli_parser.add_argument('--trace',
                                action='store_true',
                                help='traceroute destination',
                                default=False)
    ios_cli_parser.add_argument('--bgp-lookup',
                                action='store_true',
                                help='bgp table lookup',
                                default=False)
    ios_cli_parser.add_argument('--bgp-sum',
                                action='store_true',
                                help='bgp summary',
                                default=False)

    arguments = parser.parse_args()
    # pass output to selected function
    arguments.func(arguments)


def ios_cli(arguments: Namespace) -> Dict:
    # check for valid ipv4 or ipv4 prefix -> check in shared lib?
    print("== ios cli test ==")
    prefix = validate_prefix(arguments.prefix)
    if prefix.version == 6:
        print(f"IPv6 Prefix, {prefix.exploded}")
    else:
        print(f"IPv4 Prefix, {prefix.exploded}")


def frr_cli(prefix):
    # check for valid ipv4 or ipv4 prefix
    print("Frr cli")


def main():
    _execute_cli()


if __name__ == "__main__":
    main()
