import pymongo


class DataBase_for_users:
    def __init__(self):
        client = pymongo.MongoClient("localhost", 27017)
        db = client.mongo_bd
        self.users = db.users
        #self.projects = db.projects

    def inserting(self, data):
        self.users.insert_one(data)

    def finding(self):
        return self.users.find()

    def replacing(self, one_dict, new_dict):
        return self.users.replace_one(one_dict, new_dict)

    def dropping(self):
        return self.users.drop()

