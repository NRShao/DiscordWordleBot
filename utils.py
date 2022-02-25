from datetime import datetime, date
from pytz import timezone

def now():
    tz = timezone('US/Eastern')
    now = datetime.now(tz)
    return now

def get_answer_list():

  answer_list = {}

  with open('./not_bot/answer_list.txt', 'r') as answers:
    for line in answers:
      line = line.strip()
      line = line.split(' ')
      date = datetime.strptime(line[0], "%Y-%m-%d")

      answer_list[date.date()] = (line[1], line[2])
  
  return answer_list

def get_insults_list():
  insult_list = []
  with open('./not_bot/insults.txt', 'r') as insults:
    for line in insults:
      line = line.strip()
      insult_list.append(line)

  return insult_list
