from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from butchershoplabelprinter.dto.Animal import Animal


class Cut:

    def __init__(self, animal: "Animal", title: str, price_per_kg: float):
        self.animal = animal
        self.title = title
        self.price_per_kg = price_per_kg

    def __repr__(self):
        return f"Cut(animal={self.animal.title}, title={self.title}, ppkg={self.price_per_kg})"
