import os
from flask import request
from flask_restful import Resource, reqparse
from food_collection import KeyType
from meal_collection import MealCollection
import requests
import data_center

# implements the REST operations for the /meals resource
# also implements a utility static method, handling the insersion of a meal in JSON representation to the collection.
class Meals(Resource):
    # POST adds a meal to /meals and returns its ID.
    def post(self):
        return Meals.handle_json_body_request(update_existing=False)
    
    # handle all required checks and parsing operation for adding a new meal in JSON representation in the body of the request
    # param: update_existing:bool
    #               if flag is True - the method will update an existing meal.
    #               if flag is False - the method will insert the meal as a new one.
    @staticmethod
    def handle_json_body_request(update_existing : bool, key_value=None):
        # request content-type is not application/json.
        if not (request.content_type != None and 'application/json' in request.content_type): 
            return 0, 415
            
        parser = reqparse.RequestParser()
        argument_description = {MealCollection.STR_NAME: str, MealCollection.STR_APPETIZER: int, MealCollection.STR_MAIN: int, MealCollection.STR_DESSERT: int}
        for arg_name, arg_type in argument_description.items():
            parser.add_argument(arg_name, type=arg_type, location='json')
            
        args = parser.parse_args()
        arg_values = [args[arg_name] for arg_name in argument_description.keys()]

        for arg_value in arg_values: # one of the required parameters was not given or not specified correctly
            if arg_value is None:
                return -1, 422
        
        new_meal_name = args[MealCollection.STR_NAME]
        does_new_meal_name_exist = data_center.meal_collection.does_item_name_exist(new_meal_name)
        if does_new_meal_name_exist:
            if update_existing:
                old_meal_name = data_center.meal_collection.get_name_by_id(key_value)
                if new_meal_name != old_meal_name: # a meal of given name already exists (not the same as updated)
                    return -2, 422
            else: # a meal of given name already exists
                return -2, 422
            
        was_created, new_meal  = data_center.meal_collection.create_new_meal(*arg_values)

        if not was_created: # one of the sent dish IDs (appetizer, main, dessert) does not exist
            return -6, 422
        else:
            if not update_existing:
                meal_id = data_center.meal_collection.insert_item(new_meal)
                return meal_id, 201 # Created
            else:
                meal_id = data_center.meal_collection.update_existing_item(new_meal, key_value)
                return meal_id, 200 # Updated

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('diet', location='args')
        args = parser.parse_args()
        diet_name = args['diet']
        if diet_name is not None:
            api_url = '{}/diets/{}'.format(os.environ["DIET_SERVICE"], diet_name)
            response = requests.get(api_url)
            response_json = response.json()
            if (response.status_code != 200):
                return response_json, response.status_code
            
            diet_item = response_json
            return data_center.meal_collection.get_meals_by_diet_listed(diet_item), 200
        else:
            return data_center.meal_collection.retrieve_all_items_listed(), 200