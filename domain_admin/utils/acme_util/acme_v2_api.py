# -*- coding: utf-8 -*-
"""
@File    : acme_v2_api.py
@Date    : 2023-07-23

code from https://github.com/certbot/certbot/blob/master/acme/examples/http01_example.py

https://datatracker.ietf.org/doc/html/rfc8555
https://www.rfc-editor.org/rfc/rfc8555

ref:
acme-dns-tiny: https://gitlab.adorsaz.ch/adrien/acme-dns-tiny/-/tree/main

https://pypi.org/project/acme/

https://www.pyopenssl.org/en/latest/index.html

https://zhuanlan.zhihu.com/p/75032510
https://letsencrypt.org/zh-cn/docs/challenge-types/
https://datatracker.ietf.org/doc/html/rfc8555

https://github.com/Trim/acme-dns-tiny

https://github.com/shuhanghang/cdn-auto-cert

https://geeknote.net/log/posts/1426

Example ACME-V2 API for HTTP-01 challenge.

Brief:

This a complete usage example of the python-acme API.

Limitations of this example:
    - Works for only one Domain name
    - Performs only HTTP-01 challenge
    - Uses ACME-v2

Workflow:
    (Account creation)
    - Create account key
    - Register account and accept TOS
    (Certificate actions)
    - Select HTTP-01 within offered challenges by the CA server
    - Set up http challenge resource
    - Set up standalone web server
    - Create domain private key and CSR
    - Issue certificate
    - Renew certificate
    - Revoke certificate
    (Account update actions)
    - Change contact information
    - Deactivate Account
"""

import json
import os
import traceback
from datetime import datetime, timedelta

import OpenSSL
import josepy as jose
import requests
from acme import challenges, errors
from acme import client
from acme import crypto_util
from acme import messages
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from flask import g

from domain_admin.config import ACME_DIR
from domain_admin.log import logger
from domain_admin.utils import uuid_util
# This is the staging point for ACME-V2 within Let's Encrypt.
from domain_admin.utils.acme_util.challenge_type import ChallengeType
from domain_admin.utils.acme_util import key_type_enum
from domain_admin.utils.acme_util import directory_type_enum
from domain_admin.utils.acme_util.directory_type_enum import DirectoryTypeEnum
from domain_admin.utils.acme_util.key_type_enum import KeyTypeEnum
from domain_admin.utils.flask_ext.app_exception import AppException

# Constants:

# ACME V2 测试环境
# DIRECTORY_URL = 'https://acme-staging-v02.api.letsencrypt.org/directory'

# ACME V2 生产环境
# letsencrypt
DIRECTORY_URL = "https://acme-v02.api.letsencrypt.org/directory"

# zerossl
# https://zerossl.com/documentation/acme/
# DIRECTORY_URL = "https://acme.zerossl.com/v2/DV90/directory"

USER_AGENT = 'domain-admin'

# Account key size
ACC_KEY_BITS = 2048

# Certificate private key size
CERT_PKEY_BITS = 2048

# ACCOUNT_STORAGE = AccountMemoryStorage()
# {directory_type: acme_client}
# @since v1.6.52 {(user_id, directory_type): acme_client}
ACME_CACHE = {}


# account.key
def get_account_key_filename(directory_type=DirectoryTypeEnum.LETS_ENCRYPT):
    return os.path.join(ACME_DIR, directory_type + '-account.key')


# ACCOUNT_KEY_FILENAME = os.path.join(ACME_DIR, 'account.key')

# account.json
# ACCOUNT_DATA_FILENAME = os.path.join(ACME_DIR, 'account.json')
def get_account_data_filename(directory_type=DirectoryTypeEnum.LETS_ENCRYPT):
    return os.path.join(ACME_DIR, directory_type + '-account.json')


# Useful methods and classes:

def new_csr_comp(domains, pkey_pem=None):
    """
    Create certificate signing request.
    :param domains: list
    :param pkey_pem:
    :return: tuple (pkey_pem, csr_pem)
    """
    if pkey_pem is None:
        # fix: type must be an integer
        # Create private key.
        pkey = OpenSSL.crypto.PKey()
        pkey.generate_key(type=OpenSSL.crypto.TYPE_RSA, bits=CERT_PKEY_BITS)
        pkey_pem = OpenSSL.crypto.dump_privatekey(
            OpenSSL.crypto.FILETYPE_PEM, pkey)

    csr_pem = crypto_util.make_csr(pkey_pem, domains)
    return pkey_pem, csr_pem


def select_http01_chall(orderr):
    """Extract authorization resource from within order resource."""
    # Authorization Resource: authz.
    # This object holds the offered challenges by the server and their status.
    authz_list = orderr.authorizations

    for authz in authz_list:
        # Choosing challenge.
        # authz.body.challenges is a set of ChallengeBody objects.
        for i in authz.body.challenges:
            # Find the supported challenge.
            if isinstance(i.chall, challenges.HTTP01):
                return i

    raise Exception('HTTP-01 challenge was not offered by the CA server.')


def select_challenge(orderr):
    """Extract authorization resource from within order resource."""
    # Authorization Resource: authz.
    # This object holds the offered challenges by the server and their status.

    logger.info("authorizations len: %s", len(orderr.authorizations))

    challenge_map = {}

    for authz in orderr.authorizations:
        # Choosing challenge.
        # authz.body.challenges is a set of ChallengeBody objects.

        domain_challenge = []
        domain = authz.body.identifier.value
        logger.info('challenges len: %s - %s', domain, len(authz.body.challenges))

        for challenge in authz.body.challenges:
            # Find the supported challenge.

            if isinstance(challenge.chall, challenges.DNS01):
                # domain_challenge[ChallengeType.DNS01] = challenge
                domain_challenge.append(challenge)
            elif isinstance(challenge.chall, challenges.HTTP01):
                # domain_challenge[ChallengeType.HTTP01] = challenge
                domain_challenge.append(challenge)
            # elif isinstance(challenge.chall, challenges.TLSALPN01):
            #     domain_challenge[ChallengeType.TLSALPN01] = challenge

        challenge_map[domain] = domain_challenge

    logger.info(challenge_map)

    return challenge_map
    # raise Exception('{} challenge was not offered by the CA server.'.format(challenge_type))


def select_challenge_by(orderr, domain, challenge_type):
    domain_challenges = select_challenge(orderr)[domain]

    for challenge in domain_challenges:
        if challenge_type == ChallengeType.HTTP01 and isinstance(challenge.chall, challenges.HTTP01):
            return challenge
        elif challenge_type == ChallengeType.DNS01 and isinstance(challenge.chall, challenges.DNS01):
            return challenge
        else:
            raise AppException('not found challenge')


def perform_http01(client_acme, orderr):
    """Set up standalone webserver and perform HTTP-01 challenge."""

    # response, validation = challb.response_and_validation(client_acme.net.key)
    #
    # # Let the CA server know that we are ready for the challenge.
    # client_acme.answer_challenge(challb, response)

    # Wait for challenge status and then issue a certificate.
    # It is possible to set a deadline time.
    deadline = datetime.now() + timedelta(seconds=10)

    try:
        finalized_orderr = client_acme.poll_and_finalize(orderr, deadline)
    except errors.TimeoutError as e:
        logger.error(traceback.format_exc())

        raise AppException("证书获取超时")

    return finalized_orderr.fullchain_pem


def get_account_key(directory_type=DirectoryTypeEnum.LETS_ENCRYPT):
    """
    Python cryptography库及RSA非对称加密
    https://blog.csdn.net/photon222/article/details/109447327
    :return:
    """
    # account_key_filename = get_account_key_filename(directory_type)

    # if os.path.exists(account_key_filename):
    #     # load private key
    #     with open(account_key_filename, "rb") as f:
    #         private_key = serialization.load_pem_private_key(
    #             f.read(),
    #             password=None,
    #             backend=default_backend()
    #         )
    # else:
    # Create account key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=ACC_KEY_BITS,
        backend=default_backend())

    # serialized private key
    # pem = private_key.private_bytes(
    #     encoding=serialization.Encoding.PEM,
    #     format=serialization.PrivateFormat.PKCS8,
    #     encryption_algorithm=serialization.NoEncryption()
    # )

    # # store private key
    # with open(account_key_filename, 'wb') as f:
    #     f.write(pem)

    return private_key


def ensure_account_exists(client_acme, directory_type=DirectoryTypeEnum.LETS_ENCRYPT):
    """
    确保账户存在
    :param directory_type:
    :param client_acme:
    :return:
    """
    account_data_filename = get_account_data_filename(directory_type)

    if os.path.exists(account_data_filename):
        # 账户已存在
        with open(account_data_filename, 'r') as f:
            account_data = json.loads(f.read())

        try:
            account_resource = messages.RegistrationResource.from_json(account_data)

            account = client_acme.query_registration(account_resource)
        except errors.Error as e:
            # logger.debug(traceback.format_exc())
            create_account(client_acme, directory_type)
    else:
        # 账户不存在
        create_account(client_acme, directory_type)


def get_zerossl_eab():
    """
    :return:
    eg:
    {
        "success": true,
        "eab_kid": "xxx",
        "eab_hmac_key": "yyy"
    }
    """
    url = 'https://api.zerossl.com/acme/eab-credentials-email'
    res = requests.post(
        url=url,
        data={'email': "admin@domain-admin.cn"}
    )

    return res.json()


def create_account(client_acme, directory_type=DirectoryTypeEnum.LETS_ENCRYPT):
    print('create_account')

    # account_data_filename = get_account_data_filename(directory_type)

    # 参考 certbot
    if client_acme.external_account_required():
        config = get_zerossl_eab()
        print('config', config)

        eab = messages.ExternalAccountBinding.from_data(
            account_public_key=client_acme.net.key.public_key(),
            kid=config['eab_kid'],
            hmac_key=config['eab_hmac_key'],
            directory=client_acme.directory
        )
    else:
        eab = None

    new_account = messages.NewRegistration.from_data(
        terms_of_service_agreed=True,
        external_account_binding=eab
    )

    register = client_acme.new_account(new_account)

    # with open(account_data_filename, 'w') as f:
    #     f.write(json.dumps(register.to_json(), indent=2))


def get_acme_client(directory_type=DirectoryTypeEnum.LETS_ENCRYPT, key_type=KeyTypeEnum.RSA):
    current_user_id = g.user_id

    # default use letsencrypt directory_url
    if not directory_type:
        directory_type = DirectoryTypeEnum.LETS_ENCRYPT

    acme_client_key = (current_user_id, directory_type)

    if acme_client_key in ACME_CACHE:
        logger.info('directory_type exists')
        return ACME_CACHE.get(acme_client_key)

    directory_url = directory_type_enum.get_directory_url(directory_type)
    if not directory_url:
        raise AppException("not found directory_url")

    # Register account and accept TOS
    private_key = get_account_key(directory_type)

    # if key_type == KeyTypeEnum.EC:
    #     account_key = jose.JWKEC(key=private_key)
    #     public_key = account_key.key
    #     if public_key.key_size == 256:
    #         alg = jose.ES256
    #     elif public_key.key_size == 384:
    #         alg = jose.ES384
    #     elif public_key.key_size == 521:
    #         alg = jose.ES512
    #     else:
    #         raise errors.NotSupportedError(
    #             "No matching signing algorithm can be found for the key"
    #         )
    # else:
    account_key = jose.JWKRSA(key=jose.ComparableRSAKey(private_key))

    net = client.ClientNetwork(account_key, alg=jose.RS256, user_agent=USER_AGENT)

    directory = client.ClientV2.get_directory(url=directory_url, net=net)
    client_acme = client.ClientV2(directory=directory, net=net)

    create_account(client_acme, directory_type)

    # ensure_account_exists(client_acme, directory_type)
    ACME_CACHE[acme_client_key] = client_acme

    return client_acme


if __name__ == '__main__':
    print(get_zerossl_eab())
