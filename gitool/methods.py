import base64
import hashlib
import logging
import sys

from pathlib import Path

from .configuration import Configuration
from .util import list_properties

logger = logging.getLogger("gitool")


def compare(repositories, root, filename):
    """
    Compare a previously made dump with the local situation.
    """

    logger.info("Comparing repositories.")

    configurations = Configuration.from_file(filename)

    # TODO IMPLEMENT


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
        msg = "Gathering configuration of {}.".format(r)
        logger.info(msg)

        f = root / r.path / '.git' / 'config'

        data = bytes(r.path) + b"\n"
        lines.append(data)

        with open(f, 'rb') as f:
            data = f.read()

        data = base64.b64encode(data)
        data = data + b"\n"
        lines.append(data)

    if filename is None:
        lines = map(lambda s: s.decode(), lines)
        sys.stdout.writelines(lines)
        return

    dumpfile = Path(filename)

    logger.info("Calculating configuration hashes.")

    hashsum_new = hashlib.sha3_256()

    for l in lines:
        hashsum_new.update(l)

    hashsum_old = hashlib.sha3_256()

    if dumpfile.exists():
        if dumpfile.is_dir():
            logger.warning("Cannot calculate hash for existing configuration.")
        else:
            with open(filename, 'rb') as f:
                hashsum_old.update(f.read())

    if hashsum_new.digest() == hashsum_old.digest():
        logger.info("Repository configurations did not change.")
        return

    logger.info("Dumping file.")

    with open(filename, 'wb') as f:
        f.writelines(lines)


def list_repositories(repositories):
    """
    Print information about all repositories in a human readable form to
    `stdout`.
    """

    logger.info("Listing repositories.")

    for r in repositories:
        msg = "{} ({})".format(r.colored_name, r.user_name)
        print(msg)


def statistics(repositories, root):
    """
    Collect statistics about the repositories in the root directory.

    If `filename` is not specified, the data will be printed to `stdout`.
    """

    logger.info("Collecting statistics.")

    ahead = 0
    behind = 0
    dirty = 0

    for r in repositories:
        msg = "Checking {}.".format(r)
        logger.info(msg)

        try:
            ahead += (1 if r.is_ahead else 0)
            behind += (1 if r.is_behind else 0)
            dirty += (1 if r.is_dirty else 0)
        except Exception as e:
            msg = "Cannot retrieve information for {}: {}".format(r, e)
            logger.warning(msg)
            continue

    data = [ahead, behind, dirty]
    data = ','.join(map(str, data)) + "\n"

    filename = root / '.statistics'

    with open(filename, 'w') as f:
        f.write(data)


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
