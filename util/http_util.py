# -*- coding: utf-8 -*-
'''
保持一个http session，比如post登录后，可以后续进行需要授权（登录）的操作 
'''
import base64
import os
import re
import sys
import tempfile
import threading
import time
import urllib
from time import sleep
from urllib.parse import urlparse

import requests
import urllib3
from loguru import logger
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3.util.retry import Retry

logger.add('./logs/' + os.path.basename(sys.argv[0]) + ".log", rotation="50 MB", enqueue=True)
from retrying import retry
import urllib.request

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class HttpUtil(object):
    def __init__(self):
        pass

    def get_302_url(self, url):
        """
        获取图片的302真实地址

        :param param1: this is a first param
        :param param2: this is a second param
        :returns: this is a description of what is returned
        :raises keyError: raises an exception
        @author： jhuang
        @time：8/9/2019
        """

        import urllib.request
        proxy_support = urllib.request.ProxyHandler({'sock5': '127.0.0.1:1080'})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        res = urllib.request.urlopen(url)
        finalurl = res.geturl()
        return (finalurl)


class HttpClass():

    def __init__(self, user='', pwd='', headers='', timeout=120, verify=False):
        """
        | ##@函数目的: HTTP 初始化
        | ##@参数说明： 
        | ##@返回值：HTTP 句柄
        | ##@函数逻辑：
        | ##@开发人：jhuang
        | ##@时间：
        """
        self.session = requests.session()
        self.retry_session(retries=3)  # 设置重试次数

        self.headers = headers
        if user != '':
            self.session.auth = (user, pwd)
        if self.headers == '':
            self.headers = {
                # "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            }
        self.timeout = timeout
        self.verify = verify
        self.cookies = {}
        self.proxies = {}

        # {"http": "http://%s" % ip_port, "https": "http://%s" % ip_port}

    def set_proxy(self, proxies={}):

        if isinstance(proxies, dict):
            self.proxies = proxies
        else:
            self.proxies = {"http": "http://%s" % proxies, "https": "http://%s" % proxies}

        logger.debug('设置代理：%s' % (self.proxies))

    def set_headers(self, headers):
        # logger.debug('header：%s' % (headers))
        self.headers = headers

    def load_chrome_cookie(self, cookie_str):
        # 解析chrome cookie
        self.cookies = {}  # 初始化cookies字典变量
        for line in cookie_str.split(';'):  # 按照字符：进行划分读取
            # 其设置为1就会把字符串拆分成2份
            name, value = line.strip().split('=', 1)
            self.cookies[name] = value  # 为字典cookies添加内容
        return self.cookies

    def load_cookie_from_file(self, cookie_file):
        f = open(r'%s' % cookie_file, 'r')  # 打开所保存的cookies内容文件
        self.cookies = self.load_chrome_cookie(f.read())
        return self.cookies

    def gen_url_filename(self, url, fix_ext_text='.jpg'):
        # 生成一个下载保存的临时文件名，用于下载时候保存
        # 扩展名默认补全
        path = urlparse(url).path
        ext = os.path.splitext(path)[1]
        if len(ext) < 2:
            ext = fix_ext_text
        file = tempfile.mktemp() + ext
        return file

    def get_url_filename(self, url, fix_ext_text='.jpg'):

        filename = os.path.basename(url)

        return filename

    def urlencode(self, params):
        """
        将字典里面所有的键值转化为query-string格式

        :param params: data = {
            'word': wd,
            'tn': '71069079_1_hao_pg',
            'ie': 'utf-8'
        }
        :param param2: this is a second param
        :returns: string, key=value&key=value
        :raises keyError: raises an exception
        @author： jhuang  ; WeChat:ajun-guo
        @time：7/16/2019
        """
        # payload = {'username': 'administrator', 'password': 'xyz'}
        # result = urlencode(payload, quote_via=quote_plus)
        query_string = urllib.parse.urlencode(params)
        return query_string

    def close(self):
        '''
        关闭连接
        '''
        self.session.close()

    #         logger.info ('关闭连接')

    def __del__(self):
        self.close()

    def retry_session(self, retries, backoff_factor=0.3, status_forcelist=(500, 502, 503, 504)):

        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        return self.session

    def post(self, url, payload={}):
        """
        | ##@函数目的: post
        | ##@参数说明： 
        payload = {
           'os_username': 'jhuang', 
           'os_password': 'debug.', 
           'os_destination':'',
           'atl_token':'',
           'login':'%E7%99%BB%E5%BD%95'
         }
        | ##@返回值：
        | ##@函数逻辑：
        | ##@开发人：jhuang
        | ##@时间：
        """

        # logger.debug(self.proxies)
        # logger.debug(self.cookies)
        r = self.session.post(url, data=payload, headers=self.headers, timeout=self.timeout, verify=self.verify,
                              proxies=self.proxies, cookies=self.cookies)
        return (r, r.text.encode('utf8'))

    def get(self, url, params={}):
        """
        | ##@函数目的: HTTP get
        | ##@参数说明： 
        | ##@返回值：
        | ##@函数逻辑：
        | ##@开发人：jhuang
        | ##@时间：
        """

        start_time = time.time()
        logger.debug(url)
        r = self.session.get(url, cookies=self.cookies, headers=self.headers, timeout=self.timeout, verify=self.verify,
                             proxies=self.proxies, params=params)
        respone_time = time.time() - start_time
        return (r, r.text.encode('utf8'), respone_time, r.content)

    @retry(stop_max_attempt_number=20, wait_fixed=6)
    def get_web_status(self, url):
        """
        | ##@函数目的: 检查web是否可以访问
        | ##@参数说明：
        | ##@返回值：返回HTTPcode 无论是多少都任务是web服务可以访问
        | ##@函数逻辑：
        | ##@开发人：jhuang
        | ##@时间：
        """
        try:
            r = self.session.get(url, stream=True, headers=self.headers, timeout=self.timeout, verify=self.verify)
            status_code = str(r.status_code)
        except Exception as e:
            status_code = ''
        return str(status_code)

    def status_code(self, url):
        """
        | ##@函数目的: 状态码
        | ##@参数说明：
        | ##@返回值：
        | ##@函数逻辑：
        | ##@开发人：jhuang
        | ##@时间：
        """
        status_code = ''
        try:
            r = self.session.get(url, stream=True, headers=self.headers, timeout=self.timeout, verify=self.verify)
            status_code = str(r.status_code)
        except Exception as e:
            logger.debug(e)
            # status_code = get_except(e, False)
        return str(status_code)

    def get_remote_file_size(self, url):
        """
        | ##@函数目的: 获取远程文件大小
        | ##@参数说明：
        | ##@返回值：
        | ##@函数逻辑：
        | ##@开发人：jhuang
        | ##@时间：
        """

        RemoteFileSize = 0
        try:
            r = self.session.get(url, stream=True, headers=self.headers, timeout=self.timeout, verify=self.verify)
            RemoteFileSize = int(r.headers['content-length'])
        except:
            RemoteFileSize = -1
        return RemoteFileSize

    def get_download_info(self, url, local_file):
        """
        |##desc: 获取下载信息
        |##:param: None
        |##:return: None
        |##@author： jhuang  ; WeChat:ajun-guo
        |##@time：2017-07-22
        """
        RemoteFileSize = self.get_remote_file_size(url)
        logger.debug
        RemoteFileSize
        if RemoteFileSize == 0: return False
        get_file_size1 = ''  # get_file_size(local_file)
        logger.debug
        get_file_size1
        sleep(1)
        get_file_size2 = ''  # get_file_size(local_file)
        logger.debug
        int(get_file_size2), int(get_file_size1)
        speed = covert_bytes(int(get_file_size2) - int(get_file_size1)) + '/s'
        percent = int(get_file_size2) * 100 / int(RemoteFileSize)
        complete = False
        logger.debug('监控到正在下载...远程文件大小：%s,本地文件大小:%s' % (RemoteFileSize, get_file_size2))
        if get_file_size2 >= RemoteFileSize or percent >= 99:
            logger.debug('监控到下载完成！远程文件大小：%s,本地文件大小:%s' % (RemoteFileSize, get_file_size2))
            complete = True
        return (RemoteFileSize, percent, speed, complete)

    def donload_b64_img(self, b64_data, file_path):
        print(' base64编码的图片保存到本地->%s' % (file_path))
        # print(b64_data)
        b64_data = re.findall('base64,(.+)', b64_data)[0]
        # print(b64_data)
        imagedata = base64.b64decode(b64_data)
        # print(imagedata)
        file = open(file_path, "wb")
        file.write(imagedata)
        file.close()

    def url_fix(self, url, protocol='https:'):
        # url修复
        url = eval(repr(url).replace('\\', '/'))
        url = url.replace('////', '//').replace('u002F', '')
        if 'http' not in url:
            url = protocol + url
        return url

    def multi_donwlod(self, downlow_data=[{'url': '', 'file': ''}], max_thrad=10):
        def download(url, file):
            self.download(url, file)

        tn = 0
        while 1:
            if tn >= len(downlow_data):
                break
            for a in downlow_data[tn:tn + max_thrad]:
                threads = []
                url = a['url']
                file = a['file']
                t = threading.Thread(target=download, args=(url, file))
                threads.append(t)
                t.start()
                # 等待主线程完成
                for t in threads:
                    t.join()

            tn = tn + max_thrad
        return downlow_data

    def download(self, url, file_path, timeout=60 * 30, progress=False):
        """
        | ##@函数目的: HTTP get
        | ##@参数说明： 
        | ##@返回值：
        | ##@函数逻辑：
        | ##@开发人：jhuang
        | ##@时间：
        """
        try:
            time_start = time.time()
            url = self.url_fix(url)
            print('下载：%s -> %s' % (url, file_path))

            r = self.session.get(url, proxies=self.proxies, stream=True, timeout=timeout, headers=self.headers,
                                 verify=self.verify, cookies=self.cookies, )

            if progress is True:
                content_size = int(float(r.headers['Content-Length'])) / 1024
            else:
                content_size = 0

            f = open(file_path, "wb")
            # logger.debug(r.status_code)
            if r.status_code != 404 and r.status_code != 401:
                for chunk in tqdm(r.iter_content(chunk_size=1024), total=content_size, unit='k'):
                    if chunk:
                        f.write(chunk)
                # logger.debug('下载文件成功!-> %s ' % (url))
                f.close()
            # elif r.status_code == 401:
            #     logger.debug('下载文件失败,状态码:%s' % (r.status_code))
            # else:
            #     logger.debug('下载文件失败,状态码:%s' % (r.status_code))
            # logger.debug('下载文件用时：%s' % (time.time() - time_start))
            return (r, file_path)
        except:
            logger.exception('遇到一个问题')


def http_get_utf8(url):
    """
    | ##@函数目的: get,解决乱码问题
    | ##@参数说明：HTTP地址
    | ##@返回值：
    | ##@函数逻辑：
    | ##@开发人：jhuang
    | ##@时间：
    """
    ohttp = HttpClass()
    ret = ohttp.get(url)
    ohttp.close()
    return ret[1]


def http_statu_code(url):
    """
    | ##@函数目的: 获取HTTP状态码 (注意这个是没带SESSION)
    | ##@参数说明：HTTP地址
    | ##@返回值：字符型HTTP状态码
    | ##@函数逻辑：
    | ##@开发人：jhuang
    | ##@时间：
    """
    if url == None or url == '':
        return 'null'
    ohttp = HttpClass(timeout=5)
    status_code = ohttp.status_code(url)
    ohttp.close()

    return status_code

# def http_get_basic_auth(url, username, password):
#     """
#     |##desc: HTTP基础认证
#     |##:param: None
#     |##:return: None
#     |##@author： jhuang  ; WeChat:ajun-guo
#     |##@time：8/31/2017
#     """
#
#     try:
#         # 创建一个密码管理者
#         password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
#         # 添加用户名和密码
#         password_mgr.add_password(None, url, username, password)
#         # 创建了一个新的handler
#         handler = urllib2.HTTPBasicAuthHandler(password_mgr)
#         # 创建 "opener"
#         opener = urllib2.build_opener(handler)
#         # 使用 opener 获取一个URL
#         opener.open(url)
#         # 安装 opener.
#         urllib2.install_opener(opener)
#         # urllib2.urlopen 使用上面的opener.
#         ret = urllib2.urlopen(url)
#         return ret.read()
#     except Exception as  e:
#         if e.code == 401:
#             return "authorization failed"
#         else:
#             raise e
#     except:
#         return None
