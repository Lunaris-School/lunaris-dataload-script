from faker import Faker
from src.utils import format_email
import random

fake = Faker('pt_BR')

class DataFactory:
    @staticmethod
    def generate_person():
        name = fake.name()
        return {
            "nome": name,
            "cpf": fake.unique.random_number(digits=11, fix_len=True),
            "email": format_email(name),
            "data": fake.date_between(start_date='-5y', end_date='today')
        }

    @staticmethod
    def generate_student():
        person = DataFactory.generate_person()
        person["matricula"] = fake.unique.random_number(digits=9, fix_len=True)
        person["genero_id"] = fake.random_int(min=1, max=3)
        return person