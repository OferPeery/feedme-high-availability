from food_collection import FoodCollection, KeyType
from dish_collection import DishCollection
import json

# Class implements the logic of the meals collection.
# Inherites from the general FoodCollection class.
class MealCollection(FoodCollection):
    # const strings for a meal's properties
    STR_APPETIZER = 'appetizer'
    STR_MAIN = 'main'
    STR_DESSERT = 'dessert'
    
    def __init__(self, db, dish_collection : DishCollection):
         super(MealCollection, self).__init__(db)
         self._dish_collection = dish_collection  # the meal collection is based on a dish collection.
         self._dish_collection.register_delete_item_event_handler(self._handle_dish_deleting)
         self._dish_types = (self.STR_APPETIZER, self.STR_MAIN, self.STR_DESSERT)
    
    def create_new_meal(self, name : str, appetizer : int, main : int, dessert : int):
        dish_ids_of_meal = (appetizer, main, dessert)
        if not self.do_dishes_exist(*dish_ids_of_meal): # one the dish IDs does not exist in the dish collection
             return False, None 
        
        # sums up the nutritive properties of all dishes compose the meal
        cal = self._calc_meal_property_from_dishes(self.STR_CAL, *dish_ids_of_meal)
        sodium = self._calc_meal_property_from_dishes(self.STR_SODIUM, *dish_ids_of_meal)
        sugar = self._calc_meal_property_from_dishes(self.STR_SUGAR, *dish_ids_of_meal) 
        new_meal = {
            self.STR_NAME: name,
            self.STR_ID: 0,
            self.STR_APPETIZER: appetizer,
            self.STR_MAIN: main,
            self.STR_DESSERT: dessert,
            self.STR_CAL: cal,
            self.STR_SODIUM: sodium,
            self.STR_SUGAR: sugar
        }
        return True, new_meal 
    
    # retuens true if all given dishes' ID exist in the dish collection.
    def do_dishes_exist(self, *dishes_id) -> bool:
         for dish_id in dishes_id:
              if not self._dish_collection.does_item_id_exist(dish_id):
                   return False
         return True

     # sums up the values of the given nutritive property of all the given dish-IDs
    def _calc_meal_property_from_dishes(self, property_name : str, *dish_ids):
         property_value = 0
         for dish_id in dish_ids:
            _, doc = self._dish_collection.find_item(KeyType.ID, dish_id)
            property_value += doc[property_name]
         return property_value
    
    # dish deleting event handler
    # when a dish is deleted from the dish collection - change to None (Null)
    # all the apearances of this dish id in all meals in the collection,
    # and the affected meal's nutritive properties - as instructed in the moodle forum.
    def _handle_dish_deleting(self, dish_id):   
        for dish_type in self._dish_types:
            query = [
                {dish_type: dish_id},
                {
                    "$set":
                        {
                            dish_type: None,
                            self.STR_CAL: None,
                            self.STR_SODIUM: None,
                            self.STR_SUGAR: None
                        }
                }
            ]
            self._db.update_many(*query)

    def get_meals_by_diet_listed(self, diet_item):
        if diet_item is None:
            return []
        
        query = [
            {
                self.STR_CAL: {"$lte": diet_item[self.STR_CAL]},
                self.STR_SODIUM: {"$lte": diet_item[self.STR_SODIUM]},
                self.STR_SUGAR: {"$lte": diet_item[self.STR_SUGAR]}
            },
            {"_id": 0}
        ]

        all_documents = self._db.find(*query)
        return list(all_documents)