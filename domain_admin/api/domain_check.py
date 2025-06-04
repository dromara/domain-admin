from flask import request, jsonify
import requests
import json
from domain_admin.log import logger
from domain_admin.utils.response import make_response

def init_api(app):
    @app.route('/api/v1/domain/check', methods=['GET'])
    def check_domain():
        """检查域名是否被封禁
        
        Returns:
            JSON: 检查结果
            {
                'code': 200/202/500,
                'msg': '结果信息'
            }
        """
        url = request.args.get('url')
        
        if not url:
            return make_response(code=202, msg='请传入URL参数')
        
        try:
            # 调用腾讯安全接口检查URL
            check_url = f'https://cgi.urlsec.qq.com/index.php?m=url&a=validUrl&url={requests.utils.quote(url)}'
            headers = {'Content-Type': 'application/json'}
            
            logger.info(f"Checking domain status for URL: {url}")
            response = requests.get(check_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            data_msg = data.get('data', '')
            
            if data_msg == 'ok':
                logger.warning(f"Domain is blocked: {url}")
                return make_response(code=202, msg='域名被封')
            else:
                logger.info(f"Domain is normal: {url}")
                return make_response(code=200, msg=data_msg)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to check domain {url}: {str(e)}")
            return make_response(code=500, msg=f'检测失败: {str(e)}')
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse response for {url}: {str(e)}")
            return make_response(code=500, msg='接口响应解析失败') 