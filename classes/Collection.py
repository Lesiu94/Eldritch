from flask import json
import sqlite3

from classes.Investigator import Investigator
from classes.Item import Item
from config import DATABASE_LOCATION


class Collection:
    basic = 1  # core set
    mOm = 0  # Mountains of Madness
    fL = 0  # Forsaken Lore
    uTp = 0  # Under the Pyramids
    sR = 0  # Strange Remnants
    sOc = 0  # Signs of Carcosa
    tD = 0  # The Dreamlands
    cIr = 0  # Cities in Ruin
    mOn = 0  # Mask od Nyarlathotep

    def reset(self):
        self.basic = 1
        self.mOm = 0
        self.fL = 0
        self.uTp = 0
        self.sR = 0
        self.sOc = 0
        self.tD = 0
        self.cIr = 0
        self.mOn = 0

    def setCollection(self, collectionJSON):
        data = json.loads(collectionJSON)
        self.reset()
        for item in data:
            setattr(self, item, 1)

    def makeItems(self):
        cur = self.getCursor()
        query = "select name, attr, qt, setid from items " + self.makeSQLWhere()
        cur.execute(query)
        rows = cur.fetchall()

        itemList = []

        for row in rows:
            item = Item()
            item.name = row["name"]
            item.attributes = row["attr"].split(", ")

            for i in range(0, row["qt"]):
                itemList.append(item)

        return itemList

    def makeConditions(self):
        cur = self.getCursor()
        query = "select name, attr, qt, setid from conditions " + self.makeSQLWhere()
        cur.execute(query)
        rows = cur.fetchall()

        conditionList = []

        for row in rows:
            item = Item()
            item.name = row["name"]
            item.attributes = row["attr"].split(", ")

            for i in range(0, row["qt"]):
                conditionList.append(item)

        return conditionList

    def makeSpells(self):
        cur = self.getCursor()
        query = "select name, attr, qt, setid from spells " + self.makeSQLWhere()
        cur.execute(query)
        rows = cur.fetchall()

        spellsList = []

        for row in rows:
            item = Item()
            item.name = row["name"]
            item.attributes = row["attr"].split(", ")

            for i in range(0, row["qt"]):
                spellsList.append(item)

        return spellsList

    def makeInvestigatorsForChoose(self):
        cur = self.getCursor()
        query = "select name, setid from investigators " + self.makeSQLWhere()
        cur.execute(query)
        rows = cur.fetchall()

        investigatorsList = []
        for row in rows:
            print(row["name"])
            investigatorsList.append(row["name"])

        return investigatorsList

    def makeInvestigatorsForGame(self, investigators):
        data = json.loads(investigators)
        cur = self.getCursor()
        query = "select name, possession1, type1, possession2, type2, possession3, type3 from investigators where name in ("
        for name in data:
            query += "'" + name + "', "
        query = query[:-2]
        query += ")"

        cur.execute(query)
        rows = cur.fetchall()
        investigatorsList = []
        for row in rows:
            investigator = Investigator()
            investigator.name = row["name"]
            if row["type1"] is not None:
                if row["type1"] == "Item":
                    print(row["possession1"])
                    investigator.items.append(row["possession1"])
                else:
                    if row["type1"] == "Spell":
                        investigator.spells.append(row["possession1"])
                    else:
                        if row["type1"] == "Condition":
                            investigator.conditions.append(row["possession1"])
                if row["type2"] is not None:
                    if row["type2"] == "Item":
                        investigator.items.append(row["possession2"])
                    else:
                        if row["type2"] == "Spell":
                            investigator.spells.append(row["possession2"])
                        else:
                            if row["type2"] == "Condition":
                                investigator.conditions.append(row["possession2"])
                    if row["type3"] is not None:
                        if row["type3"] == "Item":
                            investigator.items.append(row["possession3"])
                        else:
                            if row["type3"] == "Spell":
                                investigator.spells.append(row["possession3"])
                            else:
                                if row["type3"] == "Condition":
                                    investigator.conditions.append(row["possession3"])

            investigatorsList.append(investigator)

        return investigatorsList

    def makeSQLWhere(self):
        where = "where setid in ('Core'"

        if self.mOm:
            where += ", 'MoM'"
        if self.fL:
            where += ", 'FL'"
        if self.uTp:
            where += ", 'UtP'"
        if self.sR:
            where += ", 'SR'"
        if self.sOc:
            where += ", 'SoC'"
        if self.tD:
            where += ", 'tD'"
        if self.cIr:
            where += ", 'CiR'"
        if self.mOn:
            where += ", 'MoN'"

        where += ")"
        return where

    def getCursor(self):
        con = sqlite3.connect(DATABASE_LOCATION)
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        return cur
