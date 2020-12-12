from IPython.display import display
import pymongo
from users_info_prepare import Users_info

client = pymongo.MongoClient("localhost", 27017)
db = client.mongo_bd
users = db.users_data
projects = db.projects


def append_user(user_info: dict):
    if user_info not in users.find():
        users.insert_one(user_info)
        return 1
    else:
        return 0


def get_user(user_name: str):
    for user in users.find():
        if user.name_first == user_name.lower():
            return user
    return 0


one_user = Users_info("Егор Иванов", "программист", "питон")
one_user.main_info()

append_user(one_user.main_info_dict)
for entry in users.find():
    print(entry)


