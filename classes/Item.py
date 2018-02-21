class Item:
    name = ""
    attributes = []
    img = ""

    def __eq__(self, other):
        return self.name == other.name

    def __init__(self):
        self.name = ""
        self.attributes = []
        self.img = ""

    def checkAttr(self, attr):
        return attr in self.attributes
