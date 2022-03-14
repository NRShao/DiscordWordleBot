from datetime import datetime, date
from pytz import timezone

tz = timezone("US/Eastern")
now = datetime.now(tz).date()

answer_list = {}


def days_answer(today):
    return answer_list[today]


with open("answer_list.txt", "r") as answers:
    for line in answers:
        line = line.strip()
        line = line.split(" ")
        date = datetime.strptime(line[0], "%Y-%m-%d")

        answer_list[date.date()] = line[1]

print(days_answer(datetime.now(tz).date()))
