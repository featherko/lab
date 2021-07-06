"""Base for db with data."""
from pony.orm import Database, Optional, PrimaryKey, Required, Set

db = Database()


class Title(db.Entity):
    """Table of Flats."""

    id = PrimaryKey(int)  # noqa: A003
    title = Required(str)
    genre = Set("Genres")
    director = Set("Directors")
    cast = Set("Actors")
    score = Required(float)


class Actors(db.Entity):
    """Table of actors."""

    name = PrimaryKey(str)
    works = Set(Title)
    mean_score = Optional(float)
    frequency = Optional(int)


class Directors(db.Entity):
    """Table of directors."""

    name = PrimaryKey(str)
    works = Set(Title)
    mean_score = Optional(float)
    frequency = Optional(int)


class Genres(db.Entity):
    """Table of gengres."""

    name = PrimaryKey(str)
    works = Set(Title)
    mean_score = Optional(float)
    frequency = Optional(int)


def db_bind() -> None:
    """Binding table to db."""
    db.bind("sqlite", "Kinop.db", create_db=True)
    db.generate_mapping(create_tables=True)
