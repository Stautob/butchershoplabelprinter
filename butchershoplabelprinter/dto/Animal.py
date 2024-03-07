from butchershoplabelprinter.dto.Cut import Cut


class Animal:

    def __init__(self, animal_json):
        self.title = animal_json['title']
        self.sets = animal_json['sets']
        self.image_source = animal_json['icon_source']
        self.game_no = animal_json['gameNo']
        self.cuts = [Cut(self, p['title'], p['pricePerKg']) for p in animal_json['cuts']]

    def __repr__(self):
        return f"Animal [{self.title}, {self.sets}]"