import base64
import logging
import sys

from .configuration import Configuration
from .exception import GitoolException
from .util import list_properties

logger = logging.getLogger("gitool")


def status(repositories, check_ahead=True, check_behind=True, check_dirty=True):
    """
    Check if any repository has uncommited, unpushed or unmerged changes.
    """

    logger.info("Showing status of repositories.")

    msg = 'check_ahead={}, check_behind={}, check_dirty={}.'
    logger.debug(msg.format(check_ahead, check_behind, check_dirty))

    summary = list()

    for r in repositories:
        msg = "Checking {}.".format(r)
        logger.info(msg)

        if not r.has_urls:
            continue

        try:
            ahead = check_ahead and r.is_ahead
            behind = check_behind and not ahead and r.is_behind
            dirty = check_dirty and r.is_dirty
        except Exception as e:
            msg = "Cannot retrieve information for {}: {}".format(r, e)
            logger.warning(msg)
            continue

        properties = list()

        if ahead:
            properties.append('ahead')
        if behind:
            properties.append('behind')
        if dirty:
            properties.append('dirty')

        if len(properties) == 0:
            # If clean and up to date, move on.
            continue

        msg = "{} is " + list_properties(properties) + "."
        logger.debug(msg.format(r))
        summary.append(msg.format(r.colored_name))

    for message in summary:
        print(message)


def list_repositories(repositories):
    """
    Print information about all repositories in a human readable form to
    `stdout`.
    """

    logger.info("Listing repositories.")

    for r in repositories:
        msg = "{} ({})".format(r.colored_name, r.user_name)
        print(msg)


def dump(repositories, root, filename=None):
    """
    Dump a machine readable representation of all repositories to file
    `filename`. Dumped information will include the remote urls and default
    author information.

    If `filename` is not specified, the dump will be printed to `stdout`.
    """

    logger.info("Dumping repositories.")

    lines = list()

    for r in repositories:
        msg = "Dumping {}.".format(r)
        logger.info(msg)

        f = root / r.path / '.git' / 'config'

        data = str(r.path) + "\n"
        lines.append(data)

        with open(f, 'rb') as f:
            data = f.read()

        data = base64.b64encode(data).decode()
        lines.append(data + "\n")

    if filename is None:
        sys.stdout.writelines(lines)
    else:
        with open(filename, 'wb') as f:
            f.writelines(lines)


def compare(repositories, root, filename):
    """
    Compare a previously made dump with the local situation.
    """

    logger.info("Comparing repositories.")

    with open(filename, 'r') as f:
        lines = f.readlines()

    if len(lines) % 2 != 0:
        msg = 'Specified file is corrupt.'
        raise GitoolException(msg)

    # TODO IMPLEMENT
