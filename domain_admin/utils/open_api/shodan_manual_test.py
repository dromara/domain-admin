# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import, division

import argparse
import json

from domain_admin.config import SHODAN_API_KEY
from domain_admin.utils.open_api import shodan_api


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--domain', help='query dns/domain records by domain')
    parser.add_argument('--sha1', help='query certificate detail by sha1 fingerprint')
    parser.add_argument('--api-key', dest='api_key', default='', help='shodan api key')
    parser.add_argument('--limit', type=int, default=20, help='max records to print for --domain')
    args = parser.parse_args()

    api_key = args.api_key or SHODAN_API_KEY

    if not api_key:
        print('missing api key, pass --api-key or set SHODAN_API_KEY in env')
        return

    if not args.domain and not args.sha1:
        print('nothing to query, pass --domain or --sha1')
        return

    if args.domain:
        rows = shodan_api.search_domain_certificates(domain=args.domain, api_key=api_key)
        rows = rows or []
        print('domain={} total={}'.format(args.domain, len(rows)))
        for idx, row in enumerate(rows[:args.limit], 1):
            print('[{}] {}'.format(idx, json.dumps(row, ensure_ascii=False)))

    if args.sha1:
        cert = shodan_api.get_certificate_by_sha1(sha1=args.sha1, api_key=api_key)
        print('sha1={}'.format(args.sha1))
        print(json.dumps(cert or {}, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
