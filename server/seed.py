import random
from datetime import datetime

from app import app
from faker import Faker
from models import *

fake = Faker()

with app.app_context():
    print("Clearing database...")

    Station.query.delete()
    Platform.query.delete()
    Train.query.delete()
    Assignment.query.delete()

    print("Creating stations...")

    qc = Station(name="Queens Cross", city="Brambury")
    us = Station(name="Union Station", city="Upton Downs")

    stations = [qc, us]

    db.session.add_all(stations)
    db.session.commit()

    print("Creating platforms...")

    platforms = []

    for station in stations:
        for i in range(1, random.randint(4, 10)):
            platform = Platform(platform_num=i, station_id=station.id)
            platforms.append(platform)
    db.session.add_all(platforms)
    db.session.commit()

    print("Creating trains...")

    trains = []

    SERVICE = ["express", "local"]

    for _ in range(8):
        train = Train(
            train_num=fake.numerify(text="###"),
            service_type=random.choice(SERVICE),
            origin=fake.city(),
            destination=fake.city(),
        )
        trains.append(train)

    db.session.add_all(trains)
    db.session.commit()

    print("Creating assignments...")

    p1 = platforms[0]
    assignments = []
    arrivals = ["09::11", "09::22", "09::40", "10::05"]
    departures = ["09::18", "09::31", "09::53", "10::22"]

    for i in range(4):
        assignment = Assignment(
            arrival_time=datetime.strptime(arrivals[i], "%H::%M"),
            departure_time=datetime.strptime(departures[i], "%H::%M"),
            train_id=trains[i].id,
            platform_id=p1.id,
        )
        assignments.append(assignment)
    db.session.add_all(assignments)
    db.session.commit()

    print("Done!")
