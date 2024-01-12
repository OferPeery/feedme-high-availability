from food_collection import FoodCollection

# Class implements the logic of the dishes collection.
# Inherites from the general FoodCollection class.
class DishCollection(FoodCollection):
    # const strings for a dish's property
    STR_SIZE = 'size'

    def __init__(self, db):
        super(DishCollection, self).__init__(db)
        
    # returns a new dish item (in a dictionary format) with the given values for its properties.
    @classmethod
    def create_new_dish(cls, name : str, dish_id : int, cal : float, size : float, sodium : float, sugar : float):
        return {
            super().STR_NAME: name,
            super().STR_ID: dish_id,
            super().STR_CAL: cal,
            cls.STR_SIZE: size,
            super().STR_SODIUM: sodium,
            super().STR_SUGAR: sugar,
        }
