"""
查询考试信息
"""
import re

from bs4 import BeautifulSoup

from UESTCQuery.model import exam
from UESTCQuery.model.exam import Exam
from UESTCQuery.utils import get_semester_id, print_table
from UESTCQuery.constant import Url


# TODO: 需要重构
def __build_exam(exam_info):
    """
    构建exam实体
    :param exam_info:
    :return:
    """
    # 通过子节点的数目判断是否由具体的考试信息
    len_no_specific_info = 4
    len_no_classroom_and_seat_info = 7
    len_have_specific_info = 8

    course_id = exam_info[0].string
    course_name = exam_info[1].string

    if len(exam_info) == len_no_specific_info:
        # 无考试安排
        return Exam(
            course_id=course_id,
            course_name=course_name,
            msg=exam_info[2].string
        )

    if len(exam_info) == len_no_classroom_and_seat_info:
        return Exam(
            course_id=course_id,
            course_name=course_name,
            exam_date=exam_info[3].string,
            exam_state=exam_info[5].string
        )

    if len(exam_info) == len_have_specific_info:
        return Exam(
            course_id=course_id,
            course_name=course_name,
            exam_date=exam_info[3].string,
            exam_classroom=exam_info[4].string,
            exam_seat=exam_info[5].string,
            exam_state=exam_info[6].string
        )


def sort_exam(exam_list):
    """
    对考试信息按照周数和日期正序排序
    :param exam_list:
    :return:
    """
    return sorted(exam_list, key=lambda x: (x.year, x.month, x.day, x.start_hour, x.start_min))


def parse_exam(html):
    """
    从html中解析考试信息，并对考试信息进行排序
    :param html:
    :return: 含有考试信息的dict，查询失败返回None
    """

    soup = BeautifulSoup(html, 'html.parser')
    nodes = soup.find_all("tr", class_=re.compile("grayStyle|brightStyle"))
    if len(nodes) == 0:
        return None

    exam_list = list()
    for exam_node in nodes:
        exam_info = list(filter(lambda a: a != '\n', exam_node.contents))
        exam = __build_exam(exam_info)
        exam_list.append(exam)

    return sort_exam(exam_list)


def query_exam(session, semester_id_option=None):
    """
    查询考试信息
    :param semester_id_option: 命令行学期id option
    :param session:
    :return: 含有exam实体的list
    """
    try:
        semester_id = get_semester_id(session, Url.EXAM_URL, semester_id_option)
    except ValueError as e:
        raise e
    query_params = {
        "semester.id": semester_id,
        "examType.id": "1"
    }
    res = session.get(Url.EXAM_QUERY_URL, params=query_params)
    return parse_exam(res.text)


def print_exam(exam_list):
    """
    格式化打印exam_list
    :param exam_list: 含有exam实体的列表
    :return:
    """
    header = exam.get_header()
    data = [item.get_list() for item in exam_list]
    print_table(data, header)

