import logging

from argparse import ArgumentParser

from .exception import GitoolArgumentException

logger = logging.getLogger("gitool")


def parse_arguments():
    method_choices = [
        "compare",
        "dump",
        "list",
        "status",
    ]

    parser = ArgumentParser(
        prog="Gitool",
        description="A tool for managing git repositories."
    )
    parser.add_argument("method", type=str, choices=method_choices,
                        help="Method to run.")
    parser.add_argument("-v", "--debug", action="store_true",
                        help="Print debug information.")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Print errors and warnings only.")
    parser.add_argument("-c", "--config-file", type=str,
                        help="File to read configuration from.")
    parser.add_argument("-d", "--directory", type=str,
                        help="Directory to look for repositories in.")
    parser.add_argument("-f", "--file", type=str,
                        help="File to dump repositories to.")
    parser.add_argument("-i", "--interactive", action="store_true",
                        help="Interactively apply changes when comparing.")
    parser.add_argument("--no-ahead", action="store_true",
                        help="Do not check if repository is ahead.")
    parser.add_argument("--no-behind", action="store_true",
                        help="Do not check if repository is behind.")
    parser.add_argument("--no-dirty", action="store_true",
                        help="Do not check if repository is dirty.")

    args = parser.parse_args()

    if args.debug and args.quiet:
        msg = 'Cannot be quiet in debug mode.'
        raise GitoolArgumentException(msg)

    if args.method != 'status':
        if args.no_ahead or args.no_behind or args.no_dirty:
            msg = 'Options are not compatible with chosen method.'
            raise GitoolArgumentException(msg)

    if args.method not in ['compare']:
        if args.interactive:
            msg = 'Options are not compatible with chosen method.'
            raise GitoolArgumentException(msg)

    return args
