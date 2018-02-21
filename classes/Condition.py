class Condition:
    name = ""
    attributes = []
    img = ""

    def __init__(self):
        self.name = ""
        self.attributes = []
        self.img = ""

    def __eq__(self, other):
        return self.name == other.name