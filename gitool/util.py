import itertools
import logging

from git import Repo, InvalidGitRepositoryError

from .repository import Repository

logger = logging.getLogger("gitool")


def _list_repositories(path):
    subdirectories = [p for p in path.iterdir() if p.is_dir()]
    names = [p.name for p in subdirectories]

    if '.git' not in names:
        roots = [_list_repositories(p) for p in subdirectories]
        roots = list(itertools.chain.from_iterable(roots))
    else:
        msg = "Discovered repository at '{}'."
        logger.debug(msg.format(path))
        roots = [path]

    return roots


def get_repositories(path):
    paths = _list_repositories(path)
    repositories = list()

    for p in paths:
        try:
            repo = Repo(str(p))
        except InvalidGitRepositoryError:
            msg = "'{}' is not a git repository."
            logger.warning(msg.format(p))
            continue

        relative = p.relative_to(path)
        repository = Repository(relative, repo)
        repositories.append(repository)

    repositories.sort()

    return repositories


def list_properties(properties):
    if len(properties) > 1:
        return ', '.join(properties[:-1]) + ' and ' + properties[-1]
    else:
        return properties[0]
