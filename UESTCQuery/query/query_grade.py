"""
查询成绩
"""
import bs4
from bs4 import BeautifulSoup

from UESTCQuery.constant import Url
from UESTCQuery.model import grade
from UESTCQuery.model.grade import Grade
from UESTCQuery.utils import get_semester_id, print_table


def __build_grade(td_nodes):
    """
    构建grade实体
    :param td_nodes:
    :return:
    """
    if len(td_nodes) == 0:
        return None

    return Grade(
        course_id=td_nodes[3].text,
        course_name=td_nodes[4].text,
        course_type=td_nodes[5].text,
        credit=td_nodes[7].text,
        grade="".join(list(filter(lambda a: a != "\t" and a != "\n" and a != "\r", td_nodes[8].text))),
        resit_grade="".join(list(filter(lambda a: a != "\t" and a != "\n" and a != "\r", td_nodes[9].text))),
        final_grade="".join(list(filter(lambda a: a != "\t" and a != "\n" and a != "\r", td_nodes[10].text))),
        gpa="".join(list(filter(lambda a: a != "\t" and a != "\n" and a != "\r", td_nodes[11].text))),
    )


def parse_grade(text):
    """
    解析成绩信息
    :param text: 成绩html文本
    :return: 成绩list
    """

    soup = BeautifulSoup(text, 'html.parser')
    # 去除所有的span
    for match in soup.find_all("span"):
        match.unwrap()
    nodes = soup.find_all("tr")
    if len(nodes) == 0:
        return None

    grade_list = list()
    for grade_node in nodes[1:]:
        # nodes[1:] 为了过滤表格头部
        # 解析html中的td标签
        td_nodes = list(filter(lambda a: a != "\n" and a.string != "\n" if isinstance(a, bs4.NavigableString) else True,
                               grade_node.contents))
        grade = __build_grade(td_nodes)
        if grade is not None:
            grade_list.append(grade)

    return grade_list


def query_grade(session, semester_id_option=None):
    """
    查询成绩信息
    :param session: 已经登录的Session
    :param semester_id_option: 指定学期
    :return: 成绩list
    """
    try:
        semester_id = get_semester_id(session, Url.GRADE_URL, semester_id_option)
    except ValueError as e:
        raise e
    query_params = {
        "semesterId": semester_id,
        "projectType": ""
    }
    res = session.get(Url.GRADE_QUERY_URL, params=query_params)
    return parse_grade(res.text)


def print_grade(grade_list):
    """
    格式化打印grade_list
    :param grade_list: 含有grade_list实体的grade
    :return:
    """
    header = grade.get_header()
    data = [item.get_list() for item in grade_list]
    print_table(data, header)
