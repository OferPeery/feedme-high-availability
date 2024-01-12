from flask import Flask
from flask_restful import Api
from diets import Diets
from diet import Diet
import data_center

app = Flask(__name__) # initialize Flask
api = Api(app)        # create API

# associate Resources with Classes
api.add_resource(Diets, '/diets')
api.add_resource(Diet, '/diets/<string:item_key>')

# initialize the db collections and logic object for diets of the server application
data_center.init()