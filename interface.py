from users_info_prepare import Users_info
from project_info import Project


class User_interface:
    def __init__(self, user):
        self.user = user # user_info one user

    def make_project(self, name: str, sphere: str):
        project = Project(name, sphere, self.user)
        self.user.projects.append(project)
        self.user.update_users_v(0.1, sphere) # for creating a project v increase

    # save interests in projects
    def like_other_project(self, project):
        sphere_project = project.sphere
        try:
            sphere_ind = self.user.spheres.index(sphere_project)
            self.user.interests[sphere_ind] += 0.02
        except ValueError:
            self.user.spheres.append(sphere_project)
            self.user.interests.append(0.02)
        except KeyError:
            self.user.spheres.append(sphere_project)
            self.user.interests.append(0.02)

# testing
random_user = Users_info("Иванова Милана", "программист", ["кулинария"], [0.05])
second_random = Users_info("Пирожкова Милана", "повар", ["кулинария"], [0.04])

random_project = Project("готовка_с_пирожковой", "программирование", second_random)
random_second_project = Project("готовка_с_пирожковой", "кулинария", second_random)

interface = User_interface(random_user)
interface.make_project("готовка", "кулинария")
# check before likes
print("Check what interest one user has:")
for int in range(len(random_user.interests)):
    print(random_user.spheres[int], random_user.interests[int])

print("\nHere one user likes two projects in кулинария and программирование spheres \n")
interface.like_other_project(random_project)
interface.like_other_project(random_second_project)
# after likes
print("Check what interest one user has now")
for int in range(len(random_user.interests)):
    print(random_user.spheres[int], random_user.interests[int])
