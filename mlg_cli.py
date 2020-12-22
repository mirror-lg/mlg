"""
Execute library commands from cli
"""

import argparse
import getpass
from typing import Dict
from argparse import Namespace

from mirror_lg.lib.helpers import Helper
from mirror_lg.lib.ios.ios_lib import IosLib
from mirror_lg.api.ios_api import IosApi
from mirror_lg.lib.frr.frr_lib import FrrLib
from mirror_lg.api.frr_api import FrrApi
from mirror_lg.logging_decorator import error_logging


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
                                       description='specific network operating '
                                                   'system commands')

    ios_cli_parser = subparsers.add_parser('ios_cli',
                                           help='Run commands on legacy Cisco '
                                                'ios devices')

    ios_cli_parser.set_defaults(func=ios_cli)
    ios_cli_parser.add_argument('--sh_ip_route',
                                action='store_true',
                                help='route table lookup',
                                default=False)
    ios_cli_parser.add_argument('--trace',
                                action='store_true',
                                help='traceroute destination',
                                default=False)
    ios_cli_parser.add_argument('--sh_ip_bgp',
                                action='store_true',
                                help='bgp table lookup',
                                default=False)
    ios_cli_parser.add_argument('--sh_bgp_sum',
                                action='store_true',
                                help='bgp summary',
                                default=False)
    ios_cli_parser.add_argument('--backup',
                                action='store_true',
                                help='backup ios config',
                                # help=argparse.SUPPRESS,
                                default=False)

    frr_cli_parser = subparsers.add_parser('frr_cli',
                                           help='Run commands on frr devices')
    frr_cli_parser.set_defaults(func=frr_cli)
    frr_cli_parser.add_argument('--sh_ip_route',
                                action='store_true',
                                help='route table lookup',
                                default=False)



    arguments = parser.parse_args()

    def _load_config():
        """
        Load ssh key (if exists) or ask for password
        """
        ssh_key: str = None
        # config load from yaml file
        if not ssh_key:
            # populate clear text password, if required
            arguments.password = getpass.getpass()

    # load the key from file.
    # else:
    # arguments.ssh_key =

    _load_config()

    # instantiate the correct class
    if "ios_cli" in arguments.func.__name__:
        caller = IosLib(target_device=arguments.target,
                        username=arguments.username,
                        password=arguments.password)
    elif "frr_cli" in arguments.func.__name__:
        caller = FrrLib(target_device=arguments.target,
                        username=arguments.username,
                        password=arguments.password)

    # pass outputs to selected function
    arguments.func(arguments, caller)


def ios_cli(arguments: Namespace, caller) -> Dict:
    # pylint: disable=too-many-branches
    ios_api = IosApi(caller)
    helper = Helper()
    for key, value in vars(arguments).items():
        if key == 'trace' and value is True:
            cmd = key
            prefix = helper.validate_prefix(arguments.prefix)
            if prefix.version == 6:
                output = ios_api.show_ipv6_traceroute(cmd, prefix.exploded)
            else:
                output = ios_api.show_ipv4_traceroute(cmd, prefix.exploded)
        elif key == 'sh_ip_route' and value is True:
            cmd = key
            prefix = helper.validate_prefix(arguments.prefix)
            if prefix.version == 6:
                output = ios_api.show_ipv6_route(cmd, prefix.exploded)
            else:
                output = ios_api.show_ipv4_route(cmd, prefix.exploded)
        elif key == 'sh_ip_bgp' and value is True:
            cmd = key
            prefix = helper.validate_prefix(arguments.prefix)
            if prefix.version == 6:
                output = ios_api.show_ipv6_bgp(cmd, prefix.exploded)
            else:
                output = ios_api.show_ipv4_bgp(cmd, prefix.exploded)
        elif key == 'sh_bgp_sum' and value is True:
            cmd = key
            prefix = helper.validate_prefix(arguments.prefix)
            if prefix.version == 6:
                output = ios_api.show_ipv6_bgp_sum(cmd, prefix.exploded)
            else:
                output = ios_api.show_ipv4_bgp_sum(cmd, prefix.exploded)

    print(output)


def frr_cli(arguments: Namespace, caller) -> Dict:
    frr_api = FrrApi(caller)
    helper = Helper()
    for key, value in vars(arguments).items():
        if key == 'sh_ip_route' and value is True:
            cmd = key
            prefix = helper.validate_prefix(arguments.prefix)
            if prefix.version == 6:
                output = frr_api.show_ipv6_route(cmd, prefix.exploded)
            else:
                output = frr_api.show_ipv4_route(cmd, prefix.exploded)

    print(output)


@error_logging
def main():
    _execute_cli()


if __name__ == "__main__":
    main()
