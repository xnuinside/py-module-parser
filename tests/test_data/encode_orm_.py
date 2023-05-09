import databases
import orm
import sqlalchemy

database = databases.Database("sqlite:///db.sqlite")
metadata = sqlalchemy.MetaData()


class Note(orm.Model):
    __tablename__ = "notes"
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    text = orm.String(max_length=100, index=True)
    completed = orm.Boolean(default=False)


class Album(orm.Model):
    __tablename__ = "album"
    __metadata__ = metadata
    __database__ = database

    id = orm.Integer(primary_key=True)
    name = orm.String(max_length=100)


class Track(orm.Model):
    __tablename__ = "track"
    __metadata__ = metadata
    __database__ = database

    id = orm.Integer(primary_key=True)
    album = orm.ForeignKey(Album)
    title = orm.String(max_length=100)
    position = orm.Integer()


class Organisation(orm.Model):
    __tablename__ = "org"
    __metadata__ = metadata
    __database__ = database

    id = orm.Integer(primary_key=True)
    ident = orm.String(max_length=100)


class Team(orm.Model):
    __tablename__ = "team"
    __metadata__ = metadata
    __database__ = database

    id = orm.Integer(primary_key=True)
    org = orm.ForeignKey(Organisation)
    name = orm.String(max_length=100)


class Member(orm.Model):
    __tablename__ = "member"
    __metadata__ = metadata
    __database__ = database

    id = orm.Integer(primary_key=True)
    team = orm.ForeignKey(Team)
    email = orm.String(max_length=100)
