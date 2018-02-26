import re
from collections import namedtuple
import tabulate

from UESTCQuery.constant.Format import TABLE_WIDTH

INFOS = ["code", "teacher", "name", "room", "week", "day", "time"]
Course = namedtuple("course", INFOS)


COURSE_BASIC_INFO = re.compile(r"""activity = new TaskActivity\("(?P<code>\d+)","(?P<teacher>.+)",".+","(?P<name>.+)\(.+\)",".+","(?P<room>.+)","(?P<week>\d+)"\);""")
COURSE_SCHEDULE = re.compile(r"""index =(?P<day>\d)\*unitCount\+(?P<time>\d);""")

def _info_to_course(basic_info, schedule):
    info = basic_info.groupdict()
    info.update(schedule.groupdict())
    info["day"] = int(info["day"])
    info["time"] = int(info["time"])
    return Course(**info)

def _parse(html):
    html = html.split("\n")

    courses = []
    basic_info = None
    for line in html:
        extract_info = COURSE_BASIC_INFO.search(line)
        if extract_info is not None:
            basic_info = extract_info
        schedule = COURSE_SCHEDULE.search(line)
        if schedule is not None:
            courses.append(_info_to_course(basic_info, schedule))

    return courses

def clip_str(s):
    if len(s) > TABLE_WIDTH:
        s = s[:TABLE_WIDTH]
    return s


class Curriculum(object):
    def __init__(self, init):
        if isinstance(init, str):
            self._internal = _parse(init)
        if isinstance(init, list):
            self._internal = init

    def gather_by(self, info_name, info):
        assert info_name in INFOS
        if info_name == "week":
            courses = [course
                    for course in self._internal
                    if course._asdict()["week"][info] == "1"]
        else:
            courses = [course
                    for course in self._internal
                    if course._asdict()[info_name] == info]
        return Curriculum(courses)

    def is_empty(self):
        return len(self._internal) == 0

    def render(self, week=1):
        courses = self.gather_by("week", week)
        table = [["" for _ in range(7)] for _ in range(12)]
        for day in range(0, 7):
            for time in range(0, 12):
                course = courses.gather_by("day", day).gather_by("time", time)
                if not course.is_empty():
                    name = clip_str(course._internal[0].name)
                    room = clip_str(course._internal[0].room)
                    format_str = "{name:^{width}}\n{room:^{width}}".format(
                        name=name, room=room, width=TABLE_WIDTH)
                    table[time][day] = format_str 

        print(
            tabulate.tabulate(
                table,
                headers=("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"),
                showindex=(
                    "8:30-9:15",
                    "9:20-10:05",
                    "10:20-11:05", 
                    "11:10-11:55", 
                    "14:30-15:15", 
                    "15:20-16:05", 
                    "16:20-17:05", 
                    "17:10-17:55", 
                    "19:30-20:15", 
                    "20:20-21:05", 
                    "21:10-21:55", 
                    "22:00-22:45", 
                ),
                tablefmt="fancy_grid",
                stralign="center"
            )
        )

