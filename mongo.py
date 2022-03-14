from ast import Num
from pymongo import MongoClient
from enum import Enum
import os, utils

cluster = MongoClient(os.getenv("MONGO"))
database = cluster["WordleBot"]
recordCollection = database["WordleRecords"]
userCollection = database["WordleUsers"]


class State(Enum):
    DEFAULT = 0
    ANSWERED = 1
    RECORDED = 2


def insert_wordle_record(guild, answer, tri, num, date, user):
    if recordCollection.find_one({"user_id": user.id, "date": str(date)}) != None:
        return None
    record = {
        "user_id": user.id,
        "user_name": user.name,
        "guild_id": guild.id,
        "guild_name": guild.name,
        "word": answer[1],
        "wordle_num": answer[2],
        "date": str(answer[0]),
        "state": State.RECORDED.value,
        "trinary": tri,
        "num_guesses": num,
    }
    insert = recordCollection.insert_one(record)
    return insert


def get_user_list(guild):
    users = recordCollection.distinct("user_id", {"guild_id": guild.id})
    return users


def get_answer_count(userid):
    query = {"user_id": userid, "state": State.RECORDED.value}
    return recordCollection.count_documents(query)


def get_all_user_wordle_records(userid):
    query = {"user_id": userid, "state": State.RECORDED.value}
    if recordCollection.count_documents(query) == 0:
        return None
    records = recordCollection.find(query)
    return records


def get_average_num_guesses(userid):
    records = get_all_user_wordle_records(userid)
    if records == None:
        return None
    sum = 0
    count = 0
    for record in records:
        sum += record["num_guesses"]
        count += 1
    return sum / count
