import argparse
import sys
import os


from UESTCQuery.login import login
from UESTCQuery.query.query_grade import print_grade, query_grade
from UESTCQuery.query.query_exam import query_exam, print_exam
from UESTCQuery.query.query_curriculum import query_curriculum

cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)


def exec_query(args_option):
    username = args.username
    password = args.password
    s = login(username, password)

    if args_option.exam:
        try:
            print_exam(query_exam(s, args.semester))
        except Exception as e:
            print("ERROR: " + str(e))
        finally:
            if s is not None:
                s.close()
            return

    if args_option.grade:
        # 查询成绩
        try:
            print_grade(query_grade(s, args.semester))
        except Exception as e:
            print("ERROR:" + str(e))
        finally:
            if s is not None:
                s.close()
            return

    if args_option.curriculum:
        # 查询课表
        try:
            curriculum = query_curriculum(s, args.semester)
            if args_option.week:
                curriculum.render(int(args_option.week))
            else:
                curriculum.render()
        except Exception as e:
            print("ERROR:" + str(e))
        finally:
            if s is not None:
                s.close()
            return



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="portal username")
    parser.add_argument("password", help="portal password")

    parser.add_argument("-e", "--exam", help="get exam time list", action="store_true")
    parser.add_argument("-g", "--grade", help="get grade list", action="store_true")
    parser.add_argument("-c", "--curriculum", help="get curriculum list", action="store_true")
    parser.add_argument("-s", "--semester", help="specify semester")
    parser.add_argument("-w", "--week", help="specify week")

    args = parser.parse_args()
    exec_query(args)
