import csv
import random

from pets.models import Pet
from services.models import Veterinary, Synology, Groomer, Shelter
from django.core.management import BaseCommand


class Command(BaseCommand):
    models = (Synology, Veterinary, Shelter, Groomer,)
    type_list = ("cat", "dog", "pig", "hom", "ano")
    pet_names = ("Ванька", "Борька", "Монстр", "Мурка", "Сивка", "Мухтар",)
    breeds = ("жирная", "сиамская", "овчарка", "пятнистая", "мелкий",)
    ages = [1, 2, 3, 5, 6]
    weights = [1, 2, 3, 4,]
    owners = [1, 2, 3]
    is_sterilized = [0, 1, 0, 1]
    is_vaccinated = [1, 0, 1, 0]
    base_data = {"user": 1, "price": 500, "work_time_from": "10",
                 "work_time_to": "12", 'about': "я хороший и добрый.",
                 "published": False, }
    synology_data = {
        "task": "t",
        "format": "i",
        "duration": 1,
    }
    groomer_data = {
        "grooming_type": "h",
        "duration": 1,
    }
    veterinary_data = {
        "pet_type": "cat",
        "duration": 1,
    }
    shelter_data = {
        "pet_type": "cat",
    }
    # data = [base_data.update(specialist_data) for specialist_data in
    #         (synology_data, groomer_data, veterinary_data, shelter_data)]

    def generate(self) -> None:
        pet_list = [Pet(
            type=random.choice(self.type_list),
            breed=random.choice(self.breeds),
            name=random.choice(self.pet_names),
            age=random.choice(self.ages),
            weight=random.choice(self.weights),
            is_sterilized=random.choice(self.is_sterilized),
            is_vaccinated=random.choice(self.is_vaccinated),
            owner_id=random.choice(self.owners),
        ) for _ in range(10)]
        Pet.objects.bulk_create(pet_list, ignore_conflicts=True)
        print("done!")

    def handle(self, *args, **options) -> None:
        self.generate()
