import ssl
from ftplib import FTP_TLS
import OpenSSL
from domain_admin.enums.ssl_type_enum import SSLTypeEnum
from domain_admin.utils import domain_util, time_util, json_util
from domain_admin.utils.cert_util import cert_common

# 默认的ftp端口
DEFAULT_FTP_PORT = 21

# www.
WWW_WITH_DOT = 'www.'

def verify_cert(cert, domain):
    """
    验证证书和域名是否匹配
    :param cert:
    :param domain:
    :return:
    """
    # 检查 颁发对象 域名（CN） 备用域名（SAN）
    common_name = cert.get_subject().commonName

    dns_names = cert_common.get_certificate_san(cert)

    if common_name not in dns_names:
        dns_names.insert(0, common_name)

    # 申请域名为www.domain.com的证书同时支持保护domain.com
    if common_name.startswith(WWW_WITH_DOT):
        not_www_common_name = common_name[len(WWW_WITH_DOT):]
        if not_www_common_name not in dns_names:
            dns_names.append(not_www_common_name)
    else:
        www_common_name = WWW_WITH_DOT + common_name
        if www_common_name not in dns_names:
            dns_names.append(www_common_name)

    for dns_name in dns_names:
        domain_checked = domain_util.verify_cert_common_name(dns_name, domain)
        if domain_checked:
            return True

    return False


def get_ftp_cert(
        domain,
        host=None,
        port=DEFAULT_FTP_PORT,
        timeout=3,
        #ssl_type=SSLTypeEnum.SSL_TLS
):
    """
    不验证证书，仅验证域名
    支持通配符
    :param ssl_type:
    :param domain: str
    :param host: str
    :param port: int
    :param timeout: int
    :return:
    """
    cert = None

    if domain.startswith("https://"):
        domain = domain[len("https://"):]
    if domain.startswith("http://"):
        domain = domain[len("http://"):]
    # split port in domain
    if ":" in domain:
        temp_list = domain.split(":")
        domain = temp_list[0]
        try:
            port = int(temp_list[-1])
        except Exception:
            print("Illegal port ", temp_list[-1])
    # 默认参数
    host = host or domain

    try:
        # 创建 FTPS 连接
        ftps = FTP_TLS(context=ssl._create_stdlib_context(cert_reqs=ssl.CERT_REQUIRED))
        ftps.connect(host, port)
        ftps.auth()  # 发送 AUTH TLS 命令
        # ftps.prot_p()  # 切换到安全数据连接

        ## 获取 SSL socket 并提取证书
        
        # 获取证书信息的字典
        # cert = ftps.sock.getpeercert(binary_form=False)  # cert_reqs=ssl.CERT_REQUIRED 才能获取到解析好的字典证书
        # # print(cert)

        # 获取二进制证书,bytes类型
        cert = ftps.sock.getpeercert(binary_form=True)
        # 从二进制生产PEM格式
        pem_cert = ssl.DER_cert_to_PEM_cert(cert)
        print(pem_cert)

        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, pem_cert.encode())

    except Exception as e:
        print(f"Get cert error: {e}")
    
    try:
        ftps.quit()
    except Exception as e:
        ftps.close()
        
    return cert


def get_ftp_cert_by_ftplib(
        domain,
        host=None,
        port=DEFAULT_FTP_PORT,
        timeout=3,
        #ssl_type=SSLTypeEnum.SSL_TLS
):
    """
    不验证证书，仅验证域名
    支持通配符
    :param ssl_type:
    :param domain: str
    :param host: str
    :param port: int
    :param timeout: int
    :return:
    """
    # get
    cert = get_ftp_cert(domain, host, port, timeout)

    # verify
    domain_checked = verify_cert(cert, domain)

    if not domain_checked:
        raise Exception("domain not verified")

    return {
        'start_date': time_util.parse_time(cert.get_notBefore().decode()),
        'expire_date': time_util.parse_time(cert.get_notAfter().decode()),
    }
