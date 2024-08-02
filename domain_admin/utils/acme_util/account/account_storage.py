# -*- coding: utf-8 -*-
"""
@File    : account_storage.py
@Date    : 2024-08-01
code from certbot
"""
import functools
import os
import shutil
from abc import abstractmethod, ABCMeta
from typing import List, Optional, Dict

import josepy as jose
from acme.client import ClientV2
from acme import fields as acme_fields, messages
from domain_admin.log import logger
from domain_admin.utils.acme_util.account import errors
from domain_admin.utils.acme_util.account.account import Account


class AccountStorage(metaclass=ABCMeta):
    """Accounts storage interface."""

    @abstractmethod
    def find_all(self) -> List['Account']:  # pragma: no cover
        """Find all accounts.

        :returns: All found accounts.
        :rtype: list

        """
        raise NotImplementedError()

    @abstractmethod
    def load(self, account_id: str) -> 'Account':  # pragma: no cover
        """Load an account by its id.

        :raises .AccountNotFound: if account could not be found
        :raises .AccountStorageError: if account could not be loaded

        :returns: The account loaded
        :rtype: .Account

        """
        raise NotImplementedError()

    @abstractmethod
    def save(self, account: 'Account', client: ClientV2) -> None:  # pragma: no cover
        """Save account.

        :raises .AccountStorageError: if account could not be saved

        """
        raise NotImplementedError()


class AccountMemoryStorage(AccountStorage):
    """In-memory account storage."""

    def __init__(self, initial_accounts: Optional[Dict[str, Account]] = None) -> None:
        self.accounts = initial_accounts if initial_accounts is not None else {}

    def find_all(self) -> List[Account]:
        return list(self.accounts.values())

    def save(self, account: Account, client: ClientV2) -> None:
        if account.id in self.accounts:
            logger.debug("Overwriting account: %s", account.id)
        self.accounts[account.id] = account

    def load(self, account_id: str) -> Account:
        try:
            return self.accounts[account_id]
        except KeyError:
            raise errors.AccountNotFound(account_id)


class AccountFileStorage(AccountStorage):
    """Accounts file storage.

    :ivar certbot.configuration.NamespaceConfig config: Client configuration

    """

    def __init__(self, config) -> None:
        self.config = config
        os.makedirs(config.accounts_dir)

    def _account_dir_path(self, account_id: str) -> str:
        return self._account_dir_path_for_server_path(account_id, self.config.server_path)

    def _account_dir_path_for_server_path(self, account_id: str, server_path: str) -> str:
        accounts_dir = self.config.accounts_dir_for_server_path(server_path)
        return os.path.join(accounts_dir, account_id)

    @classmethod
    def _regr_path(cls, account_dir_path: str) -> str:
        return os.path.join(account_dir_path, "regr.json")

    @classmethod
    def _key_path(cls, account_dir_path: str) -> str:
        return os.path.join(account_dir_path, "private_key.json")

    @classmethod
    def _metadata_path(cls, account_dir_path: str) -> str:
        return os.path.join(account_dir_path, "meta.json")

    def _find_all_for_server_path(self, server_path: str) -> List[Account]:
        accounts_dir = self.config.accounts_dir_for_server_path(server_path)
        try:
            candidates = os.listdir(accounts_dir)
        except OSError:
            return []

        accounts = []
        for account_id in candidates:
            try:
                accounts.append(self._load_for_server_path(account_id, server_path))
            except errors.AccountStorageError:
                logger.debug("Account loading problem", exc_info=True)

        if not accounts and server_path in constants.LE_REUSE_SERVERS:
            # find all for the next link down
            prev_server_path = constants.LE_REUSE_SERVERS[server_path]
            prev_accounts = self._find_all_for_server_path(prev_server_path)
            # if we found something, link to that
            if prev_accounts:
                try:
                    self._symlink_to_accounts_dir(prev_server_path, server_path)
                except OSError:
                    return []
            accounts = prev_accounts
        return accounts

    def find_all(self) -> List[Account]:
        return self._find_all_for_server_path(self.config.server_path)

    def _symlink_to_account_dir(self, prev_server_path: str, server_path: str,
                                account_id: str) -> None:
        prev_account_dir = self._account_dir_path_for_server_path(account_id, prev_server_path)
        new_account_dir = self._account_dir_path_for_server_path(account_id, server_path)
        os.symlink(prev_account_dir, new_account_dir)

    def _symlink_to_accounts_dir(self, prev_server_path: str, server_path: str) -> None:
        accounts_dir = self.config.accounts_dir_for_server_path(server_path)
        if os.path.islink(accounts_dir):
            os.unlink(accounts_dir)
        else:
            os.rmdir(accounts_dir)
        prev_account_dir = self.config.accounts_dir_for_server_path(prev_server_path)
        os.symlink(prev_account_dir, accounts_dir)

    def _load_for_server_path(self, account_id: str, server_path: str) -> Account:
        account_dir_path = self._account_dir_path_for_server_path(account_id, server_path)
        if not os.path.isdir(account_dir_path):  # isdir is also true for symlinks
            if server_path in constants.LE_REUSE_SERVERS:
                prev_server_path = constants.LE_REUSE_SERVERS[server_path]
                prev_loaded_account = self._load_for_server_path(account_id, prev_server_path)
                # we didn't error so we found something, so create a symlink to that
                accounts_dir = self.config.accounts_dir_for_server_path(server_path)
                # If accounts_dir isn't empty, make an account specific symlink
                if os.listdir(accounts_dir):
                    self._symlink_to_account_dir(prev_server_path, server_path, account_id)
                else:
                    self._symlink_to_accounts_dir(prev_server_path, server_path)
                return prev_loaded_account
            raise errors.AccountNotFound(f"Account at {account_dir_path} does not exist")

        try:
            with open(self._regr_path(account_dir_path)) as regr_file:
                regr = messages.RegistrationResource.json_loads(regr_file.read())
            with open(self._key_path(account_dir_path)) as key_file:
                key = jose.JWK.json_loads(key_file.read())
            with open(self._metadata_path(account_dir_path)) as metadata_file:
                meta = Account.Meta.json_loads(metadata_file.read())
        except IOError as error:
            raise errors.AccountStorageError(error)

        return Account(regr, key, meta)

    def load(self, account_id: str) -> Account:
        return self._load_for_server_path(account_id, self.config.server_path)

    def save(self, account: Account, client: ClientV2) -> None:
        """Create a new account.

        :param Account account: account to create
        :param ClientV2 client: ACME client associated to the account

        """
        try:
            dir_path = self._prepare(account)
            self._create(account, dir_path)
            self._update_meta(account, dir_path)
            self._update_regr(account, dir_path)
        except IOError as error:
            raise errors.AccountStorageError(error)

    def update_regr(self, account: Account) -> None:
        """Update the registration resource.

        :param Account account: account to update

        """
        try:
            dir_path = self._prepare(account)
            self._update_regr(account, dir_path)
        except IOError as error:
            raise errors.AccountStorageError(error)

    def update_meta(self, account: Account) -> None:
        """Update the meta resource.

        :param Account account: account to update

        """
        try:
            dir_path = self._prepare(account)
            self._update_meta(account, dir_path)
        except IOError as error:
            raise errors.AccountStorageError(error)

    def delete(self, account_id: str) -> None:
        """Delete registration info from disk

        :param account_id: id of account which should be deleted

        """
        account_dir_path = self._account_dir_path(account_id)
        if not os.path.isdir(account_dir_path):
            raise errors.AccountNotFound(f"Account at {account_dir_path} does not exist")
        # Step 1: Delete account specific links and the directory
        self._delete_account_dir_for_server_path(account_id, self.config.server_path)

        # Step 2: Remove any accounts links and directories that are now empty
        if not os.listdir(self.config.accounts_dir):
            self._delete_accounts_dir_for_server_path(self.config.server_path)

    def _delete_account_dir_for_server_path(self, account_id: str, server_path: str) -> None:
        link_func = functools.partial(self._account_dir_path_for_server_path, account_id)
        nonsymlinked_dir = self._delete_links_and_find_target_dir(server_path, link_func)
        shutil.rmtree(nonsymlinked_dir)

    def _delete_accounts_dir_for_server_path(self, server_path: str) -> None:
        link_func = self.config.accounts_dir_for_server_path
        nonsymlinked_dir = self._delete_links_and_find_target_dir(server_path, link_func)
        os.rmdir(nonsymlinked_dir)

    def _delete_links_and_find_target_dir(self, server_path: str,
                                          link_func: Callable[[str], str]) -> str:
        """Delete symlinks and return the nonsymlinked directory path.

        :param str server_path: file path based on server
        :param callable link_func: callable that returns possible links
            given a server_path

        :returns: the final, non-symlinked target
        :rtype: str

        """
        dir_path = link_func(server_path)

        # does an appropriate directory link to me? if so, make sure that's gone
        reused_servers = {}
        for k, v in constants.LE_REUSE_SERVERS.items():
            reused_servers[v] = k

        # is there a next one up?
        possible_next_link = True
        while possible_next_link:
            possible_next_link = False
            if server_path in reused_servers:
                next_server_path = reused_servers[server_path]
                next_dir_path = link_func(next_server_path)
                if os.path.islink(next_dir_path) and filesystem.readlink(next_dir_path) == dir_path:
                    possible_next_link = True
                    server_path = next_server_path
                    dir_path = next_dir_path

        # if there's not a next one up to delete, then delete me
        # and whatever I link to
        while os.path.islink(dir_path):
            target = filesystem.readlink(dir_path)
            os.unlink(dir_path)
            dir_path = target

        return dir_path

    def _prepare(self, account: Account) -> str:
        account_dir_path = self._account_dir_path(account.id)
        util.make_or_verify_dir(account_dir_path, 0o700, self.config.strict_permissions)
        return account_dir_path

    def _create(self, account: Account, dir_path: str) -> None:
        with util.safe_open(self._key_path(dir_path), "w", chmod=0o400) as key_file:
            key_file.write(account.key.json_dumps())

    def _update_regr(self, account: Account, dir_path: str) -> None:
        with open(self._regr_path(dir_path), "w") as regr_file:
            regr = messages.RegistrationResource(
                body={},
                uri=account.regr.uri)
            regr_file.write(regr.json_dumps())

    def _update_meta(self, account: Account, dir_path: str) -> None:
        with open(self._metadata_path(dir_path), "w") as metadata_file:
            metadata_file.write(account.meta.json_dumps())
