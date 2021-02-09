
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class NewsSourceDropDown(db.Model):
    name = db.Column(db.String(75),primary_key=True)
    URL = db.Column(db.String(75))
    bias=db.Column(db.String(15))

class NewsSource(db.Model):
    name = db.Column(db.String(75),primary_key=True)
    URL = db.Column(db.String(75))
    bias=db.Column(db.String(15))

class Authors(db.Model):
    name=db.Column(db.String(100),primary_key=True)

class Articles(db.Model):
    title=db.Column(db.String(150))
    date=db.Column(db.DateTime())
    url=db.Column(db.String(300),primary_key=True)
    bias=db.Column(db.String(15))

class Writes(db.Model):
    author=db.Column(db.String(100),db.ForeignKey(Authors.name))
    article=db.Column(db.String(300),db.ForeignKey(Articles.url))
    __table_args__ = (
        db.PrimaryKeyConstraint('author', 'article'),
        {},
    )
class Writes_For(db.Model):
    author=db.Column(db.String(100),db.ForeignKey(Authors.name))
    newssource=db.Column(db.String(75),db.ForeignKey(NewsSource.name))
    __table_args__ = (
        db.PrimaryKeyConstraint('author', 'newssource'),
        {},
    )

class Contains(db.Model):
    article=db.Column(db.String(300),db.ForeignKey(Articles.url))
    newssource=db.Column(db.String(75),db.ForeignKey(NewsSource.name))
    __table_args__ = (
        db.PrimaryKeyConstraint('article', 'newssource'),
        {},
    )