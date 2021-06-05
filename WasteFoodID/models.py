# import the standard Django Model
# from built-in library
from django.db import models

# declare a new model with a name "WasteFood"
class WasteFoodID(models.Model):
	# fields of the model
    user_id = models.IntegerField()
    weight = models.FloatField()
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    

    # renames the instances of the model
    # with their title name
    def __str__(self):
        return self.weight
