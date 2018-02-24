def get_header():
    return ["课程ID",
            "课程名称",
            "课程类型",
            "学分",
            "总评成绩",
            "补考成绩",
            "最终成绩",
            "GPA"]


class Grade:

    def __init__(self,
                 course_id,
                 course_name="",
                 course_type="",
                 credit="",
                 grade="",
                 resit_grade="",
                 final_grade="",
                 gpa=""):
        self.id = course_id
        self.name = course_name if course_name is not None else ""
        self.type = course_type
        self.credit = credit
        self.grade = grade
        self.resit_grade = resit_grade
        self.final_grade = final_grade
        self.gpa = gpa

    def get_list(self):
        return [self.id if self.id is not None else "",
                self.name,
                self.type,
                self.credit,
                self.grade,
                self.resit_grade,
                self.final_grade,
                self.gpa]

