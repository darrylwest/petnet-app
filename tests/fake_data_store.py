"""Data Source is where fixture data is generated or pulled from other loacations via API."""

import time
from datetime import datetime, timezone
from faker import Faker

from petnet_app.models.user import Version, UserModel, keygen


class FakeDataStore:
    def __init__(self):
        """Init the data store with a faker, today, etc"""
        self.fake = Faker()
        self.today = datetime.now(tz=timezone.utc)

    def birth_year(self, min_age: int = 20, max_age: int = 100):
        return self.today.year - self.fake.random_int(min_age, max_age)

    def phone(self) -> str:
        return f"{self.fake.random_int(100,999)}-{self.fake.random_int(100,999)}-{self.fake.random_int(1000, 9999)}"

    def person(self) -> tuple:
        """return first, last and eamil"""
        fname = self.fake.first_name()
        lname = self.fake.last_name()
        suffix = f"{self.fake.random_digit_above_two()}{self.fake.random_digit()}"
        email = f"{fname.lower()}.{lname.lower()}-{suffix}@{self.fake.domain_name()}"

        return (fname, lname, email)

    def user_model(self):
        now = time.time_ns()
        version = Version(
            create_date=now,
            last_update=now,
            version=1,
        )

        key = keygen.route_key()
        first_name, last_name, email = self.person()
        model = UserModel(
            key=key,
            version=version,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=self.phone(),
            birth_year=self.birth_year(),
            status="new",
        )

        return model
