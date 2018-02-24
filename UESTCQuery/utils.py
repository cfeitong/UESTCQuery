import datetime
import re
from UESTCQuery.constant import Url


def parse_semester_id_options(option):
    """解析命令行参数传入的semester范围，可解析的参数示例：2015-2016-2"""
    option_pattern = re.compile("(.+)-(.+?)")
    result = re.findall(option_pattern, option)
    if len(result) == 0:
        raise ValueError("semester format is incorrect!! example: 2015-2016-2")
    year = result[0][0]
    name = result[0][1]
    return year, name


def parse_semester_id(json_ids, semester_id_option=None):
    """从json_ids中解析对应Semester Id"""
    if semester_id_option is not None:
        # 指定学期
        try:
            query_year, query_name = parse_semester_id_options(semester_id_option)
        except ValueError as e:
            raise e
    else:
        # 没有指定学期，默认获取最新学期的ID
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month

        query_year = str(year - 1) + '-' + str(year) if month <= 2 else str(year - 1) + '-' + str(year)
        if month <= 2 or month >= 9:
            query_name = '1'
        else:
            query_name = '2'

    pattern = re.compile("{id:([0-9]{2,3}),schoolYear:\"%s\",name:\"%s\"}" % (query_year, query_name))
    result = pattern.findall(json_ids)
    if len(result) != 0:
        return result[0]
    else:
        return None


def get_semester_id(session, get_cookie_url, semester_id_option=None):
    """获得学期的ID"""
    session.get(get_cookie_url)
    params = {
        'tagId': 'semesterBar1967188691Semester',
        'dataType': 'semesterCalendar',
        'value': session.cookies['semester.id'],
        'empty': 'false'
    }
    ids = session.post(Url.SEMESTER_ID_QUERY_URL, params).text
    return parse_semester_id(ids, semester_id_option)


def print_table(dataset, header=None, col_tab=3, encode_type="gbk"):
    """
    打印表格式数据
    :param dataset: 表格数据
    :param header: 表格头部，当表格头部为None的时候默认以[COL1,COL2...]作为头部
    :param col_tab: 列之间的空格数
    :param encode_type: 输出的编码格式
    :return:
    """
    table = list()
    col_tab = 0 if col_tab < 0 else col_tab

    if header is None:
        if dataset is not None or len(dataset) == 0:
            # 计算表格的列数，用于生成头部
            max_row_len = max(len(i) for i in dataset)
            header = ["COL" + str(i) for i in range(max_row_len)]
        else:
            raise ValueError("Table header is None and no dataset")

    table.append(header)
    for item in dataset:
        table.append(item)

    # 如果没有数据，只打印头部
    if dataset is None or len(dataset) == 0:
        for item in header:
            # 打印头部
            print('{0:{width}s}'.format(item, width=len(item.encode(encode_type)) + col_tab), end="")
        print()
        return

    # 找到每一列中的最长长度, 确定每一列对齐所需要的宽度
    col_max_len = __find_max_len_in_col(table, header, encode_type)

    for list_in_table in table:
        for i in range(len(header)):
            # 每一列之后空出col_tab个字节的长度， length为每一个字符串需要补齐的长度
            length = col_max_len[i] + col_tab - len(list_in_table[i].encode(encode_type)) + len(list_in_table[i])
            print('{0:{width}s}'.format(list_in_table[i], width=length), end="")
        print()


def __find_max_len_in_col(table, header, encode_type):
    # 这一行的意思是将每一列字符串以encode_type编码格式编码，然后获得最长的长度，所有的最长长度组成一个list
    # 如果table中某一个list的长度< header的长度，则该字符串长度返回0
    return [max([len(row[i].encode(encode_type)) if i < len(row) else 0 for row in table]) for i in range(len(header))]


