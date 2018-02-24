import re

import requests

from UESTCQuery import config
from UESTCQuery.constant import Url


def __check_login(res):
    """
    检查是否登录成功
    :param res:
    :return: 登录成功为True，登录失败为False
    """
    login_success_title = "电子科技大学信息门户"

    pattern = "<title>(.*)</title>"
    result = re.compile(pattern).findall(res.text)
    if len(result) != 0 and result[0] == login_success_title:
        return True
    else:
        return False


def __login_parse_params(html, patterns):
    """根据传入的patterns解析对应的html，返回需要的参数"""

    parse_results = {}
    for (key, value) in patterns.items():
        pattern = re.compile(value)
        result = pattern.findall(html)
        if len(result) != 0:
            parse_results[key] = result[0]
        else:
            parse_results[key] = ""
    return parse_results


def __login_post(s, username, password, login_params):
    """
    向信息门户提交用户名和密码，进行登录
    :param s: 创建的session
    :param username: 用户名
    :param password: 密码
    :param login_params: 登录所需的参数
    :return: 登录成功为True， 登录失败为False
    """
    login_params['username'] = username
    login_params['password'] = password
    res = s.post(Url.PORTAL_INDEX_URL, login_params)
    return res.status_code == 200 and __check_login(res)


def __login_get_params(session):
    """
    获取登录需要的POST参数
    :param session
    :return: 含有登录参数的字典
    """
    patterns = {
        'lt': '<.*?name=\"lt\" value=\"(.*?)\"/>',
        'dllt': '<.*?name=\"dllt\" value=\"(.*?)\"/>',
        'execution': '<.*?name=\"execution\" value=\"(.*?)\"/>',
        '_eventId': '<.*?name=\"_eventId\" value=\"(.*?)\"/>',
        'rmShown': '<.*?name=\"rmShown\" value=\"(.*?)\">'
    }
    res = session.get(Url.PORTAL_INDEX_URL)
    return __login_parse_params(res.text, patterns)


def login(username, password):
    """
    登录信息门户和教务系统
    :param username: 用户名
    :param password: 密码
    :return: 登陆成功返回带有cookie的session，登录失败返回None
    """
    if username == "" or password == "":
        raise ValueError("error: username or password is null")
    s = requests.session()
    s.headers.update(config.REQUESTS_COMMON_HEADER)

    login_params = __login_get_params(s)
    if __login_post(s, username, password, login_params):
        # 登录教务系统
        try:
            s.get(Url.EAMS_INDEX_URL, timeout=20)
        except requests.Timeout:
            s.close()
            raise TimeoutError("error: connect eams timeout")
        return s
    else:
        return None
