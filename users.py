from yargy import Parser, rule, and_, not_
from yargy.interpretation import fact
from yargy.predicates import gram
from yargy.relations import gnc_relation
from yargy.pipelines import morph_pipeline
from IPython.display import display


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

Position = fact(
    "Position",
    ["position"],
)

Sphere = fact(
    "Sphere",
    ["domen"]
)

known_positions = [
    'управляющий директор',
    'вице-мэр',
    'повар'
]

known_spheres = [
    "IT",
    "лингвистика",
    "робототехника",
    "инжинерия",
]

POSITION = morph_pipeline(known_positions)

SPHERE = morph_pipeline(known_spheres)

gnc = gnc_relation()

NAME = rule(
    FIRST.interpretation(
        Name.first
    ).match(gnc),
    LAST.interpretation(
        Name.last
    ).match(gnc)
).interpretation(
    Name
)

SPHERE = rule(
    SPHERE.interpretation(
        Sphere.domen.inflected()
    ),
).interpretation(
    Sphere
)


POSITION = rule(
    POSITION.interpretation(
        Position.position.inflected()
    ),
).interpretation(
    Position
)


NAME = rule(
    gram('Name').interpretation(
        Name.first.inflected()
    ),
    gram('Surn').interpretation(
        Name.last.inflected()
    )
).interpretation(
    Name
)

users_name = "Егор Иванов"
users_profession = "управляющий директор"
users_sphere = "кулинария"

name_parser = Parser(NAME)
position_parser = Parser(POSITION)
sphere_parser = Parser(SPHERE)

matched_name = name_parser.findall(users_name)
matched_position = position_parser.findall(users_profession)
matched_sphere = sphere_parser.findall(users_sphere)

if not list(matched_sphere):
    known_spheres.append(users_sphere)
    SPHERE = morph_pipeline(known_spheres)
    SPHERE = rule(
        SPHERE.interpretation(
            Sphere.domen.inflected()
        ),
    ).interpretation(
        Sphere
    )

    sphere_parser = Parser(SPHERE)

    matched_sphere = sphere_parser.findall(users_sphere)

for match in matched_sphere:
    print(match.fact.domen)


