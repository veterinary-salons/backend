import csv
import random

from mixer.backend.django import mixer

from pets.models import Pet
from services.models import Veterinary, Synology, Groomer, Shelter
from django.core.management import BaseCommand


class Command(BaseCommand):
    models = (Synology, Veterinary, Shelter, Groomer,)
    type_list = ("cat", "dog", "pig", "hom", "ano")
    pet_names = ("Ванька", "Борька", "Монстр", "Мурка", "Сивка", "Мухтар",)
    breeds = ("жирная", "сиамская", "овчарка", "пятнистая", "мелкий",)
    ages = [1, 2, 3, 5, 6]
    weights = [1, 2, 3, 4, ]
    owners = [1, 2, 3]
    is_sterilized = [0, 1, 0, 1]
    is_vaccinated = [1, 0, 1, 0]
    base_data = {"supplier": 1, "price": 500, "work_time_from": "10",
                 "work_time_to": "12", 'about': "я хороший и добрый.",
                 "published": False, }
    synology_data = {
        "task": "t",
        "format": "i",
        "duration": 1,
    }
    groomer_data = {
        "pet_type": "dog",
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
    pets = mixer.cycle(20).blend(Pet)
    groomers = mixer.cycle(10).blend(Groomer, pet_type=mixer.SELECT(pets), grooming_type=(mixer.RANDOM, mixer.RANDOM))
    veterinaries = mixer.cycle(10).blend(Veterinary, pet_type=mixer.SELECT(pets))
    shelters = mixer.cycle(10).blend(Shelter, pet_type=mixer.SELECT(pets))
    synology = mixer.cycle(10).blend(Synology, task=(mixer.RANDOM,), format=(mixer.RANDOM,))

    _data = ((Groomer, groomers), (Veterinary, veterinaries), (Shelter, shelters), (Synology, synology),)

    def generate(self) -> None:

        [model.objects.bulk_create(data, ignore_conflicts=True) for model, data
         in self._data]
        print("done!")

    def handle(self, *args, **options) -> None:
        self.generate()
