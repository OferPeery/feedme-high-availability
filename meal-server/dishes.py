from flask import request
from flask_restful import Resource, Api, reqparse
from dish_ninja_creator import DishNinjaCreator
import data_center

# implements the REST operations for the /dishes resource
class Dishes(Resource):
    # POST adds a dish to /dishes and returns its ID.
    def post(self):
        if not (request.content_type != None and 'application/json' in request.content_type): # request content-type is not application/json.
            return 0, 415
        
        dish_ninja_creator = DishNinjaCreator()
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json')
        args = parser.parse_args()
        dish_name = args['name']
        if dish_name == None: # 'name' parameter was not specified in the message body
            return -1, 422
        
        if data_center.dish_collection.does_item_name_exist(dish_name): # dish of given name already exists
            return -2, 422
        
        new_dish, response_error_code = dish_ninja_creator.try_create_ninja_dish(dish_name)

        if response_error_code == -3: # api.api-ninjas.com/v1/nutrition does not recognize this dish name
            return -3, 422
        elif response_error_code == -4: # api.api-ninjas.com/v1/nutrition was not reachable
            return -4, 504
        else:
            dish_id = data_center.dish_collection.insert_item(new_dish)
            if dish_id == None:
                return -2, 422 # dish of given name already exists
            return dish_id, 201 # Created
    
    # GET returns all the dishes in the collection in a JSON array
    def get(self):
        return data_center.dish_collection.retrieve_all_items_listed(), 200