from flask import Flask, render_template, request
from flask_restful import Api, Resource
from classes.Collection import Collection
from classes.Item import Item
from classes.Game import Game

from classes.htmlGenerator import makeInvestigatorsForChoose

app = Flask(__name__)
api = Api(app)
collection = Collection()
game = Game()
firstLoad = True


@app.route('/eldritch')
def collectionSite():
    return render_template('collectionSite.html', name='collection')


@app.route('/setCollection', methods=['POST'])
def setCollection():
    collection.setCollection(request.form.get('collection'))
    return 'ok'


@app.route('/chooseInvestigators', methods=['GET'])
def chooseInvestigators():
    invHtml = makeInvestigatorsForChoose(collection.makeInvestigatorsForChoose())
    return render_template('chooseInvestigators.html', name='chooseInvestigators', investigators=invHtml)


@app.route('/setInvestigators', methods=['POST'])
def setInvestigators():
    game.investigators = collection.makeInvestigatorsForGame(request.form.get('investigators'))
    game.availableItems = collection.makeItems()
    game.availableSpells = collection.makeSpells()
    game.availableConditions = collection.makeConditions()
    return 'ok'


@app.route('/startGame', methods=['GET'])
def startGame():
    if not game.started:
        game.startGame()
    return render_template('game.html', name='game', game=game)


class GameAPI(Resource):
    def post(self, inv, typ, name):
        if name != "random":
            response = game.giveStuffToInv(inv, typ, name)
        else:
            attrJSON = request.form.get('attr')
            print(attrJSON)
            response = game.giveRandomToInv(inv, typ, attrJSON)
        return response

    def delete(self, inv, typ, name):
        if inv == "shop":
            response = game.removeFromShop(name)
        else:
            if isInt(name):
                response = game.takeRandomStuffFromInv(inv, typ, int(name))
            else:
                response = game.takeStuffFromInv(inv, typ, name)
        return response


class InvestigatorAPI(Resource):
    def get(self, inv, typ):
        response = game.returnStuff(inv, typ)
        return response


def isInt(value):
    try:
        int(value)
        return True
    except:
        return False


api.add_resource(InvestigatorAPI, '/game/<string:inv>/<string:typ>')
api.add_resource(GameAPI, '/game/<string:inv>/<string:typ>/<string:name>')


if __name__ == '__main__':
    app.run()
