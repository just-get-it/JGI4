from import_export import resources
from .models import Nutrition_table

class PersonResource(resources.ModelResource):
    class Meta:
        model = Nutrition_table