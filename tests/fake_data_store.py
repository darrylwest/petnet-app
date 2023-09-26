"""Data Source is where fixture data is generated or pulled from other loacations via API."""

import time
from datetime import datetime, timezone
from faker import Faker

from petnet_app.models.user import Person, UserModel, keygen
from petnet_app.models.version import Version
from petnet_app.models.status import Status


class FakeDataStore:
    def __init__(self):
        """Init the data store with a faker, today, etc"""
        self.fake = Faker()
        self.today = datetime.now(tz=timezone.utc)

    def birth_year(self, min_age: int = 20, max_age: int = 100):
        return self.today.year - self.fake.random_int(min_age, max_age)

    def phone(self) -> str:
        return f"{self.fake.random_int(100,999)}-{self.fake.random_int(100,999)}-{self.fake.random_int(1000, 9999)}"

    def person(self) -> Person:
        """Return new Person object"""
        fname = self.fake.first_name()
        lname = self.fake.last_name()
        suffix = f"{self.fake.random_digit_above_two()}{self.fake.random_digit()}"
        email = f"{fname.lower()}.{lname.lower()}-{suffix}@{self.fake.domain_name()}"
        return Person(
            first_name=fname,
            last_name=lname,
            email=email,
            phone=self.phone(),
            birth_year=self.birth_year(),
            status=Status.new(0),
        )

    def route_key(self) -> str:
        return keygen.route_key()
        
    def user_model(self, person: Person = None) -> UserModel:
        now = time.time_ns()
        version = Version.create()

        key = keygen.route_key()
        if person is None:
            person = self.person()

        model = UserModel(
            key=key,
            version=version,
            first_name=person.first_name,
            last_name=person.last_name,
            email=person.email,
            phone=person.phone,
            birth_year=person.birth_year,
            status=person.status,
        )

        return model

    def user_models(self, count: int = 10) -> list[UserModel]:
        models = [self.user_model() for _ in range(count)]
        return models
