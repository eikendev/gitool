import logging
import functools

from colorama import Fore, Style

from .exception import GitoolException

logger = logging.getLogger("gitool")


@functools.total_ordering
class Repository:
    def __init__(self, path, repo):
        self.path = path
        self.repo = repo

    @property
    def head(self):
        head = self.repo.head.reference

        return head

    @property
    def target(self):
        target = self.head.tracking_branch()

        return target

    @property
    def user_name(self):
        try:
            value = self.repo.config_reader().get_value("user", "name")
        except Exception:
            value = None

        return value

    @property
    def user_email(self):
        try:
            value = self.repo.config_reader().get_value("user", "email")
        except Exception:
            value = None

        return value

    @property
    def urls(self):
        urls = [url for remote in self.repo.remotes for url in remote.urls]

        return urls

    @property
    def has_urls(self):
        return any(self.urls)

    def _is_parent_commit(self, base, commit):
        try:
            merge_base = self.repo.merge_base(base, commit)[0]
            msg = 'Found merge base: {}.'
            logger.debug(msg.format(merge_base))
        except IndexError:
            m = "Cannot determine merge base."
            logger.debug(m)
            raise GitoolException(m)

        is_equal = base == merge_base
        is_ancestor = self.repo.is_ancestor(merge_base, base)
        is_parent = not is_equal and is_ancestor

        return is_parent

    def _get_relevant_commits(self):
        lc = self.head.commit
        rc = self.target.commit

        return lc, rc

    @property
    def is_ahead(self):
        lc, rc = self._get_relevant_commits()
        ahead = self._is_parent_commit(lc, rc)

        return ahead

    @property
    def is_behind(self):
        lc, rc = self._get_relevant_commits()
        behind = self._is_parent_commit(rc, lc)

        return behind

    @property
    def is_dirty(self):
        dirty = self.repo.is_dirty(
            index=True,
            working_tree=True,
            untracked_files=True
        )

        return dirty

    @property
    def colored_name(self):
        s = Fore.YELLOW + str(self) + Style.RESET_ALL

        return s

    def __str__(self):
        return str(self.path)

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented

        same_path = self.path == other.path

        return same_path

    def __gt__(self, other):
        if type(self) is not type(other):
            return NotImplemented

        gte_path = self.path >= other.path

        return gte_path

    def __hash__(self):
        return hash(self.path)
