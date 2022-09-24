# -*- coding: utf-8 -*-
"""
# 查询域名证书到期情况
"""
import json
import re
import subprocess
from datetime import datetime
import traceback

from datahelper.util.render_util import Render
from dataspider.util import EmailSender
import dateparser
from operator import itemgetter

# 需要检查的域名列表
domain_list = [
    'https://36kr.com/'
]

# 到期前几天提醒
BEFORE_EXPIRE_DAYS = 3



def get_cert_expire_date(domain):
    """获取证书剩余时间"""
    info = get_cert_info(domain)

    # print(format_date(info['start_date']), '~', format_date(info['expire_date']))

    expire_date = info['expire_date']

    # 剩余天数
    # print(datetime.now())
    return {
        'domain': domain,
        'start_date': format_date(info['start_date']),
        'expire_date': format_date(info['expire_date']),
        'expire_days': (expire_date - datetime.now()).days
    }


def main():
    print('=' * 20)
    print(format_time(datetime.now()))

    has_expired_domain = False

    lst = []
    for domain in domain_list:
        try:
            info = get_cert_expire_date(domain)
            # info['domain'] = domain
            # print(info)
            lst.append(info)
            # expire_date = get_cert_expire_date(domain)
            # print(domain, info['expire_days'])
            # f.write(domain)
            # f.write(' ')
            # f.write(expire_date)
            # f.write('\n')
            if info['expire_days'] <= BEFORE_EXPIRE_DAYS:
                has_expired_domain = True
                # print('还有3天过期', domain)
                # EmailSender.send("[ssl]证书过期提醒", '域名还有3天过期: ' + domain)

        except Exception as e:
            traceback.print_exc()
            EmailSender.send("网站访问异常", str(e) + ' ' + domain)

    if has_expired_domain:
        # if True:
        lst.sort(key=itemgetter('expire_days'))

        # print(json.dumps(lst, ensure_ascii=False, indent=4))
        # f.close()

        for item in lst:
            print(item['expire_days'], item['domain'])

        html = Render().render('domain-cert-email.html', **{'list': lst})
        # with open('email.html', 'w') as f:
        #     f.write(html)

        EmailSender.send("[ssl]证书过期时间汇总", html, _subtype='html')

    # 导出域名ssl时间表
    # df = pd.DataFrame(lst)
    # df.to_csv('./domain-ssl.csv',
    #           columns=['domain', 'start_date', 'expire_date', 'expire_days'],
    #           header=['域名', '生效日期', '失效日期', '剩余天数'],
    #           index_label='序号',
    #           )


if __name__ == "__main__":
    main()
