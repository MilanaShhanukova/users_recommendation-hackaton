from users_info_prepare import Users_info
from project_info import Project


class User_interface:
    def __init__(self, user):
        self.user = user # user_info one user

    def make_project(self, name: str, sphere: str):
        project = Project(name, sphere, self.user)
        self.user.projects.append(project)
        self.user.update_users_v(0.1) # for creating a project v increase

    # save interests in projects
    def like_other_project(self, project):
        sphere_project = project.spheres
        try:
            sphere_ind = self.user.spheres.find(sphere_project)
            self.user.interests[sphere_ind] += 0.02
        except ValueError:
            self.user.spheres.append(sphere_project)
            self.user.interests.append(0.02)

