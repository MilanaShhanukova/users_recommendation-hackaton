import pymongo
import numpy as np
import csv

client = pymongo.MongoClient("localhost", 27017)
db = client.mongo_bd
users = db.users_data
projects = db.projects

# class for every project
class Project:
    def __init__(self, name: str, sphere: str, main_creator, r=0, other_creators=list()):
        self.name = name
        self.sphere = sphere
        self.r = r # save r
        self.creators = other_creators
        self.label = 0 # idea - 0, project - 1
        self.main_creator = main_creator # object user

    # add calculated creators
    def add_creators(self, update_creators: list):
        for user in update_creators:
            if user not in self.creators:
                self.creators.append(user)

    # after like - update idea r
    def update_r(self, v_user: float):
        self.r += v_user

    def make_idea_project(self):
        # compare with other projects in this sphere
        same_projects_rs = [project.r ** (-project.main_creator.v)
                            for project in projects.find() if project.spheres == self.sphere]

        if self.r ** (-self.main_creator.v) >= np.mean(same_projects_rs):
            self.label = 1
