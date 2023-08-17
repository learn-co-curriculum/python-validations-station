from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


class Station(db.Model):
    __tablename__ = "stations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    city = db.Column(db.String(80))

    def __repr__(self):
        return f"<Station {self.name}>"


class Platform(db.Model):
    __tablename__ = "platforms"

    id = db.Column(db.Integer, primary_key=True)
    platform_num = db.Column(db.Integer)
    station_id = db.Column(db.Integer, db.ForeignKey("stations.id"))

    def __repr__(self):
        return f"<Platform {self.name}>"


class Train(db.Model):
    __tablename__ = "trains"

    id = db.Column(db.Integer, primary_key=True)
    train_num = db.Column(db.String)
    service_type = db.Column(db.String)
    origin = db.Column(db.String)
    destination = db.Column(db.String)

    def __repr__(self):
        return f"<Train {self.name}>"


class Assignment(db.Model):
    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)
    arrival_time = db.Column(db.DateTime)
    departure_time = db.Column(db.DateTime)
    train_id = db.Column(db.Integer, db.ForeignKey("trains.id"))
    platform_id = db.Column(db.Integer, db.ForeignKey("platforms.id"))

    def __repr__(self):
        return f"<Assignment Train No: {self.train.train_num} Platform: {self.platform.platform_num}>"
