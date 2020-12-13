from yargy import Parser, rule, and_, not_
from yargy.interpretation import fact
from yargy.predicates import gram
from yargy.relations import gnc_relation
from yargy.pipelines import morph_pipeline
from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()

#from system
known_spheres = ["IT",
                 "лингвистика",
                 "робототехника",
                 "инжинерия"]

class Users_info:
    def __init__(self, name: str, profession: str, sphere: list, v:list):
        self.name = name
        self.profession = profession # profession of the user
        self.spheres = sphere
        self.spheres_v = {} # the spheres in which user is interested
        self.interests = [0] * len(self.spheres) # interests of the user in all spheres
        self.interests_spheres = {}
        self.known_professions = [
            'управляющий директор',
            'вице-мэр',
            'повар',
            "разработчик"
        ]
        self.projects = []
        #self.known_spheres =
        self.main_info_dict = {}
        self.v = v
        self.activity = 0
        self.gnc = gnc_relation()

    def prepare_name(self):
        Name = fact(
            'Name',
            ['first', 'last'],
        )

        LAST = and_(
            gram('Surn'),
            not_(gram('Abbr')),
        )

        FIRST = and_(
            gram('Name'),
            not_(gram('Abbr')),
        )

        NAME = rule(LAST.interpretation(
                Name.last
            ).match(self.gnc),
            FIRST.interpretation(
                Name.first
            ).match(self.gnc)
        ).interpretation(
            Name
        )

        NAME = rule(gram('Surn').interpretation(
                Name.last.inflected()
            ),
            gram('Name').interpretation(
                Name.first.inflected()
            )

        ).interpretation(
            Name
        )
        name_parser = Parser(NAME)

        return name_parser

    def prepare_profession(self):
        Profession = fact(
            "Profession",
            ["profession"],
        )

        PROFESSION = morph_pipeline(self.known_professions)

        PROFESSION = rule(
            PROFESSION.interpretation(
                Profession.profession.inflected()
            ),
        ).interpretation(
            Profession
        )

        position_parser = Parser(PROFESSION)
        return position_parser

    def prepare_sphere(self):
        Sphere = fact(
            "Sphere",
            ["domen"]
        )

        SPHERE = morph_pipeline(known_spheres)

        SPHERE = rule(
            SPHERE.interpretation(
                Sphere.domen.inflected()
            ),
        ).interpretation(
            Sphere
        )

        sphere_parser = Parser(SPHERE)
        return sphere_parser

    def get_users_professions(self):
        word = morph.parse(self.profession)[0].normal_form
        if word not in self.known_professions:
            self.known_professions.append(word)
            # update everything with new profession

        name_parser = self.prepare_profession()
        matched_profession = name_parser.findall(self.profession)

        professions = [match.fact.profession for match in matched_profession]
        return professions

    def get_users_sphere(self):
        # append new spheres in spheres_v
        for s in self.spheres:
            # clean form of s
            clean_s = morph.parse(s)[0].normal_form

            if clean_s not in known_spheres:
                known_spheres.append(clean_s)
            try:
                self.spheres_v[clean_s] = self.v[self.spheres.index(s)]
            except KeyError:
                self.spheres_v[clean_s] = 0

    def update_users_v(self, update_num: float, sphere: str):
        try:
            self.spheres_v[sphere] += update_num
        except KeyError:
            self.spheres_v[sphere] = update_num

    def calculate_activity(self, update_num: float):
        self.activity += update_num

    def main_info(self):
        self.get_users_sphere()
        self.main_info_dict["spheres"] = self.spheres_v
        self.main_info_dict["profession"] = self.get_users_professions()

        matched_name = self.prepare_name().findall(self.name)
        matched_name_ = self.prepare_name().findall(self.name)
        self.main_info_dict["name_first"] = "".join([match.fact.first for match in matched_name])
        self.main_info_dict["name_second"] = "".join([match.fact.last for match in matched_name_])
        if not self.main_info_dict["name_first"]:
            self.main_info_dict["name_first"] = self.name.split()[0].lower()
            self.main_info_dict["name_second"] = self.name.split()[1].lower()
        self.main_info_dict["activity"] = self.activity
        self.main_info_dict["projects"] = self.projects