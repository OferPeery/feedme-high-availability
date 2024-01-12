from flask_restful import Resource
from diet_collection import DietCollection
import data_center

# implements the REST operations for the /diets/{name} resource
class Diet(Resource):
    def __init__(self):
        super()
        self.diet_collection = data_center.diet_collection

    def get(self, item_key):
        found, data_to_return = self.diet_collection.find_item(item_key)
        if (found):
            return data_to_return, 200
        else:
            return f"Diet {item_key} not found", 404