import colorama
import logging

from functools import partial

from .arguments import parse_arguments
from .config import load_config, get_default_config_file, get_root_dir
from .exception import GitoolArgumentException, GitoolConfigurationException
from .logging import setup_logger
from .methods import status, list_repositories, dump, compare
from .util import get_repositories

logger = logging.getLogger("gitool")


def execute_method(args, path):
    msg = "Executing method: '{}'.".format(args.method)
    logger.debug(msg)

    repositories = get_repositories(path)

    check_ahead = not args.no_ahead
    check_behind = not args.no_behind
    check_dirty = not args.no_dirty

    methods = {
        "compare": partial(compare,
                           root=path,
                           filename=args.file),
        "dump": partial(dump,
                        root=path,
                        filename=args.file),
        "list": partial(list_repositories),
        "status": partial(status,
                          check_ahead=check_ahead,
                          check_behind=check_behind,
                          check_dirty=check_dirty),
    }

    try:
        method = methods[args.method]
    except KeyError:
        logger.error('Method does not exist.')
        exit(1)

    try:
        method(repositories)
    except KeyboardInterrupt:
        msg = 'Received keyboard interrupt.'
        logger.warning(msg)
        exit(1)


def main():
    setup_logger(logger)

    try:
        args = parse_arguments()
    except GitoolArgumentException as e:
        msg = 'Failed to parse arguments: ' + str(e)
        logger.error(msg)
        exit(1)

    if args.debug:
        logger.setLevel(logging.DEBUG)
        msg = "Application is running in debug mode."
        logger.debug(msg)
    elif args.quiet:
        logger.setLevel(logging.WARNING)

    config_file = args.config_file

    if config_file is None:
        config_file = get_default_config_file()

    config = load_config(config_file)

    logger.info("Starting Gitool.")

    def load_parameter(required, conf_section, conf_name, arg_name):
        arg = getattr(args, arg_name, None)

        if arg is not None:
            return arg

        conf = config.get(conf_section, conf_name, fallback=None)

        if not required:
            return conf
        else:
            msg = "Required argument not provided: '{}'."
            logger.error(msg.format(arg_name))
            exit(1)

    directory = load_parameter(True, 'GENERAL', 'RootDir', 'directory')

    try:
        directory = get_root_dir(directory)
    except GitoolConfigurationException as e:
        msg = "Initialization not successful: " + str(e)
        logger.error(msg)
        exit(1)

    colorama.init()

    execute_method(args, directory)
