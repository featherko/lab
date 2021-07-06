"""Fill db with data from csv file."""
import csv

from pony.orm import commit, db_session

from kino.db import Actors, Directors, Genres, Title, db_bind


def prepare_data(tbl_name: str, row: dict, t: Title) -> None:
    """Prepare data.

    In case of actors and genre we need additional preparation of data to add it relations.
    Difference is the fact that actors and genres has string of names. Converting it into list of
    str names.
    """
    if tbl_name in ["Actors", "Genre"]:
        lst = row[tbl_name].replace(", ", ",").split(",")
        for name in lst:
            add_to_db(name, tbl_name, t)
    else:
        name = row[tbl_name]
        add_to_db(name, tbl_name, t)


def add_to_db(name: str, tbl_name: str, t: Title) -> None:
    """Adding to db."""
    do = {
        "Director": Directors,
        "Actors": Actors,
        "Genre": Genres,
    }
    if not do[tbl_name].exists(name=name):
        do[tbl_name](name=name, mean_score=t.score, frequency=1, works=Title[t.id])
    else:
        do[tbl_name][name].mean_score = (do[tbl_name][name].mean_score + t.score) / 2
        do[tbl_name][name].frequency += 1
        do[tbl_name][name].works.add(Title[t.id])


@db_session
def csv_to_db() -> None:
    """Fill db.

    Using cvs dictreader, so we can reference to necessary fields as dict. Goint for each row
    and adding it to db.
    """
    with open("IMDB-Movie-Data.csv", newline="", encoding="unicode-escape") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            t = Title(
                id=row["Rank"],
                title=row["Title"],
                score=row["Rating"],
            )
            for table in ["Director", "Actors", "Genre"]:
                prepare_data(table, row, t)
        commit()


if __name__ == "__main__":
    db_bind()
    csv_to_db()
