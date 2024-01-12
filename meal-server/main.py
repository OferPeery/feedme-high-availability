from flask import Flask
from flask_restful import Api
from dishes import Dishes
from meals import Meals
from Item import Dish, Meal
import data_center

app = Flask(__name__) # initialize Flask
api = Api(app)        # create API

# associate Resources with Classes
api.add_resource(Dishes, '/dishes')
api.add_resource(Meals, '/meals')
api.add_resource(Dish, '/dishes/<int:item_key>', '/dishes/<string:item_key>')
api.add_resource(Meal, '/meals/<int:item_key>', '/meals/<string:item_key>')

# initialize the db collections and logic objects for dishes and meals of the server application
data_center.init()