from IPython.display import display
import pymongo
from users_info_prepare import Users_info
import random

client = pymongo.MongoClient("localhost", 27017)
db = client.mongo_bd
users = db.users_data
projects = db.projects
users.drop()


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


with open("names.txt", encoding="utf-8") as file:
    users_names = file.read().split('\n')
with open("professions.txt", encoding="utf-8") as file:
    professions = file.read().split('\n')
with open("spheres.txt", encoding="utf-8") as spheres:
    areas = spheres.read().split('\n')

for i in range(len(users_names)):
    name = users_names[i]
    prof = professions[i]
    sphere = areas[i].split()

    user = Users_info(name, prof, sphere, [random.uniform(0, 1)])
    user.main_info()
    append_user(user.main_info_dict)


for entry in users.find():
    print(entry)


