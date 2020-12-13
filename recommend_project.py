import random
import pymongo
import pandas as pd
from project_info import Project
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix

client = pymongo.MongoClient("localhost", 27017)
db = client.mongo_bd
users = db.users_data
projects = db.projects

all_users = []
heading = []
for entry in users.find():
    all_users.append(entry)
    heading = entry.keys()


projects_names = ["приготовление пироженных",
                  "разработка чат-бота",
                  "создание робота",
                  "разработка алгоритма",
                  "разработка рекламы",
                  "анализ рынка",
                  "разработка занятия для старшеклассников",
                  "рисование",
                  "анализ английской морфологии",
                  "разработка голосового помощника",
                  "приготовление торта"]
spheres = ["кулинария",
           "питон",
           "робототехника",
           "программирование",
           "маркетинг",
           "экономика",
           "преподавание",
           "творчество",
           "лингвистика",
           "питон",
           "кулинария"]

all_projects = []
for id_ in range(len(projects_names)):
    pr = Project(projects_names[id_], spheres[id_], main_creator=all_users[id_], r=random.randint(0, 10))
    all_projects.append(pr.__dict__.values())
    heading = pr.__dict__.keys()

df = pd.DataFrame(all_projects, columns=heading)
projects_rec = df.pivot_table(index='name',columns='sphere',values='r').fillna(0)

partner_reccom_matrix = csr_matrix(projects_rec.values)

model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute', n_neighbors=3)
model_knn.fit(partner_reccom_matrix)


# we will randomly choose one user
project_ind = 4

distances, indices = model_knn.kneighbors(projects_rec.iloc[project_ind, :].values.reshape(1, -1),
                                          n_neighbors=7)

# check for random user, result are not that obvious cause there is not so much data
random_project = projects_names[4]

for i in range(0, len(distances.flatten())):
    if i == 0:
        print(f"Recommendations for {random_project}")
    else:
        ind_project = projects_rec.index[indices.flatten()[i]]
        print(f"{i} : {ind_project} with distance {distances.flatten()[i]}")

