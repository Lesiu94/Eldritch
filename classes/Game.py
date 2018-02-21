import random
from flask import json


class Game:
    started = False
    investigators = []
    shop = []
    availableItems = []
    availableConditions = []
    availableSpells = []
    discardedItems = []
    discardedConditions = []
    discardedSpells = []

    def shuffleItems(self):
        random.shuffle(self.availableItems)

    def shuffleConditions(self):
        random.shuffle(self.availableConditions)

    def shuffleSpells(self):
        random.shuffle(self.availableSpells)

    def startGame(self):
        # print('startem items')
        self.giveStarterItems()
        # print('startem con')
        self.giveStarterConditions()
        # print('startem spells')
        self.giveStarterSpells()
        # print('shuffle con')
        self.shuffleConditions()
        # print('shuffle items')
        self.shuffleItems()
        # print('shuffle spells')
        self.shuffleSpells()
        # print('shop')
        self.makeShop()
        # print('print')
        self.printGameStat()
        self.started = True

    def printGameStat(self):
        for investigator in self.investigators:
            print(investigator.name)
            for item in investigator.items:
                print(item.name)
            for spell in investigator.spells:
                print(spell.name)
            for condition in investigator.conditions:
                print(condition.name)

        print('shop')
        for item in self.shop:
            print(item.name)

    def giveStarterItems(self):

        investigatorIndex = 0
        for investigator in self.investigators:
            tempItemList = []
            for item in investigator.items:
                index = 0
                for stuff in self.availableItems:
                    if index > len(self.availableItems) - 1:
                        index = -1
                        break
                    if stuff.name == item:
                        tempItemList.append(self.availableItems[index])
                        del self.availableItems[index]
                        break
                    if index == -1:
                        print("not found!")
                        print(investigator.name)
                        print(item)
                    index += 1
            self.investigators[investigatorIndex].items = tempItemList
            investigatorIndex += 1

    def giveStarterSpells(self):

        investigatorIndex = 0
        for investigator in self.investigators:
            tempSpellList = []
            for spell in investigator.spells:
                index = 0
                for stuff in self.availableSpells:
                    if index > len(self.availableSpells) - 1:
                        index = -1
                        break
                    if stuff.name == spell:
                        tempSpellList.append(self.availableSpells[index])
                        del self.availableSpells[index]
                        break
                    if index == -1:
                        print("not found!")
                        print(investigator.name)
                        print(spell)
                    index += 1
            self.investigators[investigatorIndex].spells = tempSpellList
            investigatorIndex += 1

    def giveStarterConditions(self):

        investigatorIndex = 0
        for investigator in self.investigators:
            tempConditionList = []
            for condition in investigator.conditions:
                index = 0
                for stuff in self.availableConditions:
                    if index > len(self.availableConditions) - 1:
                        index = -1
                        break
                    if stuff.name == condition:
                        tempConditionList.append(self.availableConditions[index])
                        del self.availableConditions[index]
                        break
                    if index == -1:
                        print("not found!")
                        print(investigator.name)
                        print(condition)
                    index += 1
            self.investigators[investigatorIndex].conditions = tempConditionList
            investigatorIndex += 1

    def makeShop(self):
        itemsInShop = len(self.shop)

        while itemsInShop < 4:
            index = 0
            for item in self.availableItems:
                if not (item.checkAttr("Artifact") or item.checkAttr("Unique")):
                    self.shop.append(self.availableItems[index])
                    del self.availableItems[index]
                    itemsInShop += 1
                    index += 1
                    break
                index += 1

    def giveStuffToInv(self, investigator, type, name):
        index = 0
        found = False

        if type == "item":
            for item in self.availableItems:
                if item.name == name:
                    found = True
                    break
                else:
                    index += 1
            if found:
                for investigatorIter in self.investigators:
                    if investigatorIter.name == investigator:
                        if not self.checkDuplicate(investigatorIter.items, name):
                            investigatorIter.items.append(self.availableItems[index])
                            del self.availableItems[index]
                            return "added"
                        else:
                            return "duplicate"
        else:
            if type == "spell":
                for spell in self.availableSpells:
                    if spell.name == name:
                        found = True
                        break
                    else:
                        index += 1
                if found:
                    for investigatorIter in self.investigators:
                        if investigatorIter.name == investigator:
                            if not self.checkDuplicate(investigatorIter.spells, name):
                                investigatorIter.spells.append(self.availableSpells[index])
                                del self.availableSpells[index]
                                return "added"
                            else:
                                return "duplicate"
            else:
                if type == "condition":
                    for condition in self.availableConditions:
                        if condition.name == name:
                            found = True
                            break
                        else:
                            index += 1
                    if found:
                        for investigatorIter in self.investigators:
                            if investigatorIter.name == investigator:
                                if not self.checkDuplicate(investigatorIter.conditions, name):
                                    investigatorIter.conditions.append(self.availableConditions[index])
                                    del self.availableConditions[index]
                                    return "added"
                                else:
                                    return "duplicate"
                else:
                    if type == "shop":
                        for item in self.shop:
                            if item.name == name:
                                found = True
                                break
                            else:
                                index += 1
                        if found:
                            for investigatorIter in self.investigators:
                                if investigatorIter.name == investigator:
                                    if not self.checkDuplicate(investigatorIter.items, name):
                                        investigatorIter.items.append(self.shop[index])
                                        del self.shop[index]
                                        self.makeShop()
                                        return "added"
                                    else:
                                        return "duplicate"

        if not found:
            return "not avaliable"

    def checkDuplicate(self, list, name):
        duplicate = False
        for element in list:
            if element.name == name:
                duplicate = True
                break
        return duplicate

    def giveRandomToInv(self, inv, type, attrJSON):
        attrList = json.loads(attrJSON)
        index = 0
        if type == "item":
            for item in self.availableItems:
                match = True
                for attr in attrList:
                    match *= item.checkAttr(attr)

                if match and (item.checkAttr("Artifact")) == ("Artifact" in attrList):
                    for investigator in self.investigators:
                        if investigator.name == inv:
                            if not self.checkDuplicate(investigator.items, item.name):
                                investigator.items.append(self.availableItems[index])
                                del self.availableItems[index]
                                return item.name + " added"
                            else:
                                index += 1
                else:
                    index += 1
            return "no avaliable"

        else:
            if type == "spell":
                for spell in self.availableSpells:
                    match = True
                    for attr in attrList:
                        match *= spell.checkAttr(attr)

                    if match:
                        for investigator in self.investigators:
                            if investigator.name == inv:
                                if not self.checkDuplicate(investigator.spells, spell.name):
                                    investigator.spells.append(self.availableSpells[index])
                                    del self.availableSpells[index]
                                    return spell.name + " added"
                                else:
                                    index += 1
                    else:
                        index += 1
                return "no avaliable"

            else:
                if type == "condition":
                    for condition in self.availableConditions:
                        match = True
                        for attr in attrList:
                            match *= condition.checkAttr(attr)
                        if match:
                            for investigator in self.investigators:
                                if investigator.name == inv:
                                    if not self.checkDuplicate(investigator.conditions, condition.name):
                                        investigator.conditions.append(self.availableConditions[index])
                                        del self.availableConditions[index]
                                        return condition.name + " added"
                                    else:
                                        if condition.name in ["Cursed", "Blessed", "Hypothermia"]:
                                            return "double " + condition.name
                                        index += 1
                        else:
                            index += 1
                    return "no avaliable"

    def takeStuffFromInv(self, inv, type, name):
        indexStuff = 0
        indexInv = 0
        if type == "item":
            for investigator in self.investigators:
                if investigator.name == inv:
                    for item in investigator.items:
                        if item.name == name:
                            self.discardedItems.append(item)
                            del self.investigators[indexInv].items[indexStuff]
                            return "deleted " + item.name
                        else:
                            indexStuff += 1
                indexInv += 1
        else:
            if type == "spell":
                for investigator in self.investigators:
                    if investigator.name == inv:
                        for spell in investigator.spells:
                            if spell.name == name:
                                self.discardedSpells.append(spell)
                                del self.investigators[indexInv].spells[indexStuff]
                                return "deleted " + spell.name
                            else:
                                indexStuff += 1
                    indexInv += 1
            else:
                if type == "condition":
                    for investigator in self.investigators:
                        if investigator.name == inv:
                            for condition in investigator.conditions:
                                if condition.name == name:
                                    self.discardedConditions.append(condition)
                                    del self.investigators[indexInv].conditions[indexStuff]
                                    return "deleted " + condition.name
                                else:
                                    indexStuff += 1
                        indexInv += 1

    def takeRandomStuffFromInv(self, inv, type, amount):
        indexInv = 0
        names = []
        if type == "item":
            for investigator in self.investigators:
                if investigator.name == inv:
                    random.shuffle(self.investigators[indexInv].items)
                    if amount > len(self.investigators[indexInv].items):
                        amount = len(self.investigators[indexInv].items)
                    for i in range(amount):
                        names.append(self.investigators[indexInv].items[0].name)
                        del self.investigators[indexInv].items[0]
                indexInv += 1
        else:
            if type == "spell":
                for investigator in self.investigators:
                    if investigator.name == inv:
                        random.shuffle(self.investigators[indexInv].spells)
                        if amount > len(self.investigators[indexInv].spells):
                            amount = len(self.investigators[indexInv].spells)
                        for i in range(amount):
                            names.append(self.investigators[indexInv].spells[0].name)
                            del self.investigators[indexInv].spells[0]
                    indexInv += 1
            else:
                if type == "condition":
                    for investigator in self.investigators:
                        if investigator.name == inv:
                            random.shuffle(self.investigators[indexInv].conditions)
                            if amount > len(self.investigators[indexInv].conditions):
                                amount = len(self.investigators[indexInv].conditions)
                            for i in range(amount):
                                names.append(self.investigators[indexInv].conditions[0].name)
                                del self.investigators[indexInv].conditions[0]
                        indexInv += 1
        return json.dumps(names)

    def returnStuff(self, inv, typ):
        names = []

        if typ == "item":
            for investigator in self.investigators:
                if investigator.name == inv:
                    for item in investigator.items:
                        names.append(item.name)
        else:
            if typ == "spell":
                for investigator in self.investigators:
                    if investigator.name == inv:
                        for spell in investigator.spells:
                            names.append(spell.name)
            else:
                if typ == "condition":
                    for investigator in self.investigators:
                        if investigator.name == inv:
                            for condition in investigator.conditions:
                                names.append(condition.name)

        return json.dumps(names)

    def removeFromShop(self, name):
        indexStuff = 0
        for item in self.shop:
                if item.name == name:
                    self.discardedItems.append(item)
                    del self.shop[indexStuff]
                    self.makeShop()
                    return "deleted " + item.name
                else:
                    indexStuff += 1

