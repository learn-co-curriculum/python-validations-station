from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata, engine_options={"echo": True})


class Station(db.Model):
    __tablename__ = "stations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    city = db.Column(db.String(80))

    def __repr__(self):
        return f"<Station {self.name}>"

    @validates("name")
    def validate_name(self, key, name):
        if not name:
            raise AssertionError("No name provided")
        if Station.query.filter(Station.name == name).first():
            raise AssertionError("Station name is already in use")
        if len(name) < 3 or len(name) > 80:
            raise AssertionError("Station name must be between 3 and 80 characters")
        return name


class Platform(db.Model):
    __tablename__ = "platforms"

    id = db.Column(db.Integer, primary_key=True)
    platform_num = db.Column(db.Integer)
    station_id = db.Column(db.Integer, db.ForeignKey("stations.id"))

    __table_args__ = (
        db.UniqueConstraint(
            "platform_num", "station_id", name="unique_platform_per_station"
        ),
    )

    def __repr__(self):
        return f"<Platform No. {self.platform_num}>"

    @validates("platform_num")
    def validate_platform_num(self, key, platform_num):
        if not isinstance(platform_num, int):
            raise AssertionError("Platform number must be an integer")
        if not 1 <= platform_num <= 20:
            raise AssertionError("Platform number must be between 1 and 20")
        return platform_num


class Train(db.Model):
    __tablename__ = "trains"

    id = db.Column(db.Integer, primary_key=True)
    train_num = db.Column(db.String)
    service_type = db.Column(db.String)
    origin = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Train {self.name}>"

    @validates("origin")
    def validate_origin(self, key, origin):
        if not origin:
            raise AssertionError("No origin provided")
        if len(origin) < 3 or len(origin) > 80:
            raise AssertionError("Origin must be between 3 and 80 characters")
        return origin

    @validates("destination")
    def validate_destination(self, key, destination):
        if not destination:
            raise AssertionError("No destination provided")
        if len(destination) < 3 or len(destination) > 80:
            raise AssertionError("Destination must be between 3 and 80 characters")
        return destination

    @validates("service_type")
    def validate_service_type(self, key, service_type):
        if not service_type:
            raise AssertionError("No service type provided")
        if service_type not in ["express", "local"]:
            raise AssertionError("Service type must be either 'express' or 'local'")
        return service_type

    def __repr__(self):
        return f"<Train {self.train_num}>"


class Assignment(db.Model):
    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)
    arrival_time = db.Column(db.DateTime)
    departure_time = db.Column(db.DateTime)
    train_id = db.Column(db.Integer, db.ForeignKey("trains.id"))
    platform_id = db.Column(db.Integer, db.ForeignKey("platforms.id"))

    __table_args__ = (
        db.UniqueConstraint(
            "platform_id", "arrival_time", name="unique_platform_assignment"
        ),
    )

    def __repr__(self):
        return f"<Assignment Train No: {self.train.train_num} Platform: {self.platform.platform_num}>"

    @validates("arrival_time", "departure_time")
    def validate_times(self, key, time):
        if key == "arrival_time" and self.departure_time and time > self.departure_time:
            raise AssertionError("Arrival time must be before departure time")
        elif key == "departure_time" and self.arrival_time and time < self.arrival_time:
            raise AssertionError("Departure time must be after arrival time")
        elif (
            key == "departure_time"
            and self.arrival_time
            and (time - self.arrival_time) > timedelta(minutes=20)
        ):
            raise AssertionError("Stay at platform must not be more than 20 minutes")
        return time

    @validates("platform_id")
    def validate_platform(self, key, platform_id):
        assignment = Assignment.query.filter(
            Assignment.platform_id == platform_id,
            Assignment.departure_time > self.arrival_time,
        ).first()
        if assignment:
            raise AssertionError("Platform must be vacant at the time of assignment")
        return platform_id
