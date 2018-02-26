"""\
查询课表
"""

import requests as rq

import UESTCQuery.constant.Url as Url
from UESTCQuery.utils import get_semester_id
from UESTCQuery.model.curriculum import Curriculum

def query_curriculum(session, semester_id_option=None):
    """
    查询课表
    :param session: 已经登录的Session
    :param semester_id_option: 指定学期
    :return: 包含课程信息的Curriculum对象
    """
    try:
        semester_id = get_semester_id(session, Url.GRADE_URL, semester_id_option)
    except ValueError as e:
        raise e
    data = {
        "ignoreHead": 1,
        "setting.kind": "std",
        "startWeek": 1,
        "project.id": 1,
        "semester.id": semester_id,
        "ids": 138150,
    }

    response = session.post(Url.CURRICULUM_QUERY_URL, data=data)
    assert response.status_code == 200

    return Curriculum(response.text)