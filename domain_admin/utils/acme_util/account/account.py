# -*- coding: utf-8 -*-
"""
@File    : account.py
@Date    : 2024-08-01
code from certbot
"""
import datetime
import hashlib
from typing import Optional, Any, cast, Mapping
import josepy as jose
import pyrfc3339
from acme import fields as acme_fields, messages
from cryptography.hazmat.primitives import serialization
import socket
import pytz


class Account:
    """ACME protocol registration.

    :ivar .RegistrationResource regr: Registration Resource
    :ivar .JWK key: Authorized Account Key
    :ivar .Meta: Account metadata
    :ivar str id: Globally unique account identifier.

    """

    class Meta(jose.JSONObjectWithFields):
        """Account metadata

        :ivar datetime.datetime creation_dt: Creation date and time (UTC).
        :ivar str creation_host: FQDN of host, where account has been created.
        :ivar str register_to_eff: If not None, Certbot will register the provided
                                        email during the account registration.

        .. note:: ``creation_dt`` and ``creation_host`` are useful in
            cross-machine migration scenarios.

        """
        creation_dt: datetime.datetime = acme_fields.rfc3339("creation_dt")
        creation_host: str = jose.field("creation_host")
        register_to_eff: str = jose.field("register_to_eff", omitempty=True)

    def __init__(self, regr: messages.RegistrationResource, key: jose.JWK,
                 meta: Optional['Meta'] = None) -> None:
        self.key = key
        self.regr = regr
        self.meta = self.Meta(
            # pyrfc3339 drops microseconds, make sure __eq__ is sane
            creation_dt=datetime.datetime.now(tz=pytz.UTC).replace(microsecond=0),
            creation_host=socket.getfqdn(),
            register_to_eff=None) if meta is None else meta

        # try MD5, else use MD5 in non-security mode (e.g. for FIPS systems / RHEL)
        try:
            hasher = hashlib.md5()
        except ValueError:
            # This cast + dictionary expansion is made to make mypy happy without the need of a
            # "type: ignore" directive that will also require to disable the check on useless
            # "type: ignore" directives when mypy is run on Python 3.9+.
            hasher = hashlib.new('md5', **cast(Mapping[str, Any], {"usedforsecurity": False}))

        hasher.update(self.key.key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)
        )

        self.id = hasher.hexdigest()
        # Implementation note: Email? Multiple accounts can have the
        # same email address. Registration URI? Assigned by the
        # server, not guaranteed to be stable over time, nor
        # canonical URI can be generated. ACME protocol doesn't allow
        # account key (and thus its fingerprint) to be updated...

    @property
    def slug(self) -> str:
        """Short account identification string, useful for UI."""
        return "{1}@{0} ({2})".format(pyrfc3339.generate(
            self.meta.creation_dt), self.meta.creation_host, self.id[:4])

    def __repr__(self) -> str:
        return "<{0}({1}, {2}, {3})>".format(
            self.__class__.__name__, self.regr, self.id, self.meta)

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, self.__class__) and
                self.key == other.key and self.regr == other.regr and
                self.meta == other.meta)
