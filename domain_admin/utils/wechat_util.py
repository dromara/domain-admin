"""
@File    : wechat_util.py
@Date    : 2025-06-04
"""
import requests

from domain_admin.log import logger


def validate_url_for_wechat(url):
    """
    调用腾讯安全接口检查URL
    return
        eg: {'data': '没有拦截该网址', 'reCode': -202}
    """
    check_url = 'https://cgi.urlsec.qq.com/index.php'

    params = {
        'm': 'url',
        'a': 'validUrl',
        'url': url
    }

    logger.info(f"Checking domain status for URL: {url}")
    response = requests.get(check_url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    logger.info(f"Checking domain status for URL: {data}")

    return data


if __name__ == '__main__':
    validate_url_for_wechat('https://github.com')
