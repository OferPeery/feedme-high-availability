from flask_restful import Resource
from food_collection import FoodCollection, KeyType
from meals import Meals
import data_center

METHOD_NOT_ALLOWED = {
    "message": "The method is not allowed for the requested URL."
}

# implements the REST operations for an abstract polymorphic item resource.
class Item(Resource):
    def __init__(self, food_collection : FoodCollection):
        super()
        self.food_collection = food_collection

    # GET retrieves a specific item from the abstract food collection
    def get(self, item_key):
        return self._operate_by_key(self.food_collection.find_item, item_key)
    
    # DELETE deletes an item from the abstract food collection
    def delete(self, item_key):
        return self._operate_by_key(self.food_collection.delete_item, item_key)
    
    # operate the given operation on an item associated with the given key (ID or Name) in its abstract food collection.
    def _operate_by_key(self, operation, item_key):
        key_type = KeyType.ID if type(item_key) == int else KeyType.NAME
        found, data_to_return = operation(key_type, item_key)
        if (found):
            return data_to_return, 200
        else:
            return -5, 404

# concrete class for the /dishes/{ID} and /dishes/{name} resources, inherites from general Item class.
class Dish(Item):
    def __init__(self):
        super(Dish, self).__init__(data_center.dish_collection)

# concrete class for the /meals/{ID} and /meals/{name} resources, inherites from general Item class.
class Meal(Item):
    def __init__(self):
        super(Meal, self).__init__(data_center.meal_collection)

    # PUT modifies a meal associated with a specific item ID.
    # valid only for /meals/{ID} resource.
    def put(self, item_key):
        if type(item_key) == int:
            return Meals.handle_json_body_request(update_existing=True, key_value=item_key)
        else:
            return METHOD_NOT_ALLOWED, 405 # PUT request with resource /meal/{name} is not allowed.