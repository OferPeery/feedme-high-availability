from flask import request
from flask_restful import Resource, reqparse
from diet_collection import DietCollection
import data_center

# implements the REST operations for the /diets resource
class Diets(Resource):
    # POST adds a diet to /diets
    def post(self):
        parser = reqparse.RequestParser()
        argument_description = {DietCollection.STR_NAME: str,
                                DietCollection.STR_CAL: float,
                                DietCollection.STR_SODIUM: float,
                                DietCollection.STR_SUGAR: float}
        for arg_name, arg_type in argument_description.items():
            parser.add_argument(arg_name, type=arg_type, location='json')
        
        args = parser.parse_args()
        arg_values = [args[arg_name] for arg_name in argument_description.keys()]

        diet_name = args[DietCollection.STR_NAME]
        if data_center.diet_collection.does_item_name_exist(diet_name): # a meal of given name already exists
            return "Diet already exists", 422 # According to Moodle forum
        
        new_diet  = data_center.diet_collection.create_new_diet(*arg_values)
        diet_id = data_center.diet_collection.insert_item(new_diet)
        return f"Diet {diet_name} was created successfully", 201 # Created

    def get(self):
        return data_center.diet_collection.retrieve_all_items_listed(), 200