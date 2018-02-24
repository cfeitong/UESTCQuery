import re


def get_header():
    return ["课程ID", "课程名称", "考试时间", "考试教室", "考试座位号", "考试状态"]


class Exam:
    def __init__(self, course_id, course_name, exam_date="", exam_classroom="", exam_seat="", exam_state="", msg=" "):
        self.id = course_id
        self.course_name = course_name
        self.date = exam_date
        self.classroom = exam_classroom
        self.seat = exam_seat
        self.state = exam_state
        self.msg = msg
        self.year, self.month, self.day = self.parse_date()
        self.start_hour, self.start_min = self.parse_start_time()

    def parse_date(self):
        """解析出考试年、月和日"""
        if self.date == "":
            return 0, 0, 0
        pattern = re.compile(r".*([0-9]{4})-([0-9]{2})-([0-9]{2}).*")
        result = pattern.findall(self.date)
        if len(result) == 0:
            return 0, 0, 0
        return int(result[0][0]), int(result[0][1]), int(result[0][2])

    def parse_start_time(self):
        if self.date == "":
            return 0, 0
        pattern = re.compile(r".*? ([0-9]{2}):([0-9]{2}).*")
        result = pattern.findall(self.date)
        if len(result) == 0:
            return 0, 0
        return int(result[0][0]), int(result[0][1])

    def get_list(self):
        return [self.id, self.course_name, self.date, self.classroom, self.seat, self.state]

    def __str__(self):
        if self.msg == "":
            return self.id + "\t" + \
                   self.course_name + "\t" + \
                   self.date + "\t" + \
                   self.classroom + "\t" + \
                   self.seat + "\t" + \
                   self.state + "\t"
        else:
            return self.id + "\t" + \
                   self.course_name + "\t" + \
                   self.msg
