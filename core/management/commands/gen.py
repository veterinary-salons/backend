import random

from core.constants import Default

from mixer.backend.django import mixer

from pets.models import Pet
from services.models import Veterinary, Synology, Groomer, Shelter
from django.core.management import BaseCommand
import petname


class Command(BaseCommand):
    def generate(self) -> None:
        pet_names = (petname.generate() for _ in range(10))
        pets = mixer.cycle(10).blend(Pet, name=(pet for pet in pet_names))
        grooming_type = (gtype for gtype in Default.GROOMING_TYPE)
        mixer.cycle(4).blend(
            Groomer,
            pet_type=(pet.type for pet in pets),
            grooming_type=grooming_type,
        )
        mixer.cycle(5).blend(Veterinary, pet_type=(pet.type for pet in pets))
        mixer.cycle(5).blend(
            Shelter, pet_type=(pet.type for pet in pets), about=mixer.RANDOM
        )
        mixer.cycle(5).blend(
            Synology,
            task=(lambda: [random.choice(Default.SYNOLOGY_TASKS)]),
            format=(lambda: [random.choice(Default.SYNOLOGY_FORMAT)]),
        )
 

    def handle(self, *args, **options) -> None:
        self.generate()
