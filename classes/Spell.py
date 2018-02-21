class Spell:
    name = ""
    attributes = []

    def __eq__(self, other):
        return self.name == other.name

    def __init__(self):
        self.name = ""
        self.attributes = []

