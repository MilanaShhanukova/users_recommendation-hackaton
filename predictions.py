import pymongo
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix


with open("spheres.txt", encoding="utf-8") as file:
    known_spheres = file.read().split("\n")

client = pymongo.MongoClient("localhost", 27017)
db = client.mongo_bd
users = db.users_data
projects = db.projects

all_users = []
heading = []
for entry in users.find():
    all_users.append(entry)
    heading = entry.keys()


def matrix():
    all_interests_users = []
    for user in all_users:
        users_interests = user['spheres'].keys()

        interest_matrix = [0] * len(known_spheres)
        for ind, s in enumerate(known_spheres):
            if s in users_interests:
                interest_matrix[ind] = user['spheres'][s]

        all_interests_users.append(interest_matrix)
    matrix = pd.DataFrame(np.array(all_interests_users), columns=known_spheres)
    return matrix

partner_reccom = matrix()

partner_reccom_matrix = csr_matrix(partner_reccom.values)

# read about algorithm and try different
model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute', n_neighbors=3)
model_knn.fit(partner_reccom_matrix)


# we will randomly choose one user
user_ind = 4

distances, indices = model_knn.kneighbors(partner_reccom.iloc[user_ind, :].values.reshape(1, -1),
                                          n_neighbors=7)

# check for random user, result are not that obvious cause there is not so much data
random_user = all_users[4]

for i in range(0, len(distances.flatten())):
    if i == 0:
        print(f"Recommendations for {all_users[user_ind]['name_first'] + ' ' + all_users[user_ind]['name_second']}")
    else:
        ind_person = partner_reccom.index[indices.flatten()[i]]
        user_found = all_users[ind_person]["name_first"] + " " + all_users[user_ind]["name_second"]
        print(f"{i} : {user_found} with distance {distances.flatten()[i]}")

