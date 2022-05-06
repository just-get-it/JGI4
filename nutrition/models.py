from django.db import models

class Nutrition_table(models.Model):
    Product = models.CharField(max_length=30, null=True, blank=True)
    Quantity = models.IntegerField(null=True, blank=True)
    Unit = models.CharField(max_length=30, null=True, blank=True)
    Kcal = models.IntegerField(null=True, blank=True)
    Protein = models.IntegerField(null=True, blank=True)
    Carbs = models.IntegerField(null=True, blank=True)
    Fat = models.IntegerField(null=True, blank=True)
    Vit_A = models.IntegerField(null=True, blank=True)
    Vit_B1 = models.IntegerField(null=True, blank=True)
    Vit_B2 = models.IntegerField(null=True, blank=True)
    Vit_B3 = models.IntegerField(null=True, blank=True)
    Vit_B5 = models.IntegerField(null=True, blank=True)
    Vit_B6 = models.IntegerField(null=True, blank=True)
    Vit_B9 = models.IntegerField(null=True, blank=True)
    Vit_B12 = models.IntegerField(null=True, blank=True)
    Vit_C = models.IntegerField(null=True, blank=True)
    Vit_D = models.IntegerField(null=True, blank=True)
    Vit_E = models.IntegerField(null=True, blank=True)
    Vit_K = models.IntegerField(null=True, blank=True)
    Choline = models.IntegerField(null=True, blank=True)
    Calcium = models.IntegerField(null=True, blank=True)
    Copper = models.IntegerField(null=True, blank=True)
    Iron = models.IntegerField(null=True, blank=True)
    Magnesium = models.IntegerField(null=True, blank=True)
    Manganese = models.IntegerField(null=True, blank=True)
    Phosphorus = models.IntegerField(null=True, blank=True)
    Potassium = models.IntegerField(null=True, blank=True)
    Selenium = models.IntegerField(null=True, blank=True)
    Sodium = models.IntegerField(null=True, blank=True)
    Zinc = models.IntegerField(null=True, blank=True)
    Water = models.IntegerField(null=True, blank=True)
    Fiber = models.IntegerField(null=True, blank=True)
    Cholesterol = models.IntegerField(null=True, blank=True)
    Saturated_fat = models.IntegerField(null=True, blank=True)
    MonoUns_fat = models.IntegerField(null=True, blank=True)
    PolyUns_fat = models.IntegerField(null=True, blank=True)
    Sugars = models.IntegerField(null=True, blank=True)
    Glycemic_Index = models.IntegerField(null=True, blank=True)
    Comments = models.CharField(max_length=30, null=True, blank=True)
    Translation_product_name = models.CharField(max_length=30, null=True, blank=True)
    Price = models.IntegerField(null=True, blank=True)
    preference=models.CharField(max_length=30, null=True, blank=True)
    meal_type=models.CharField(max_length=30, null=True, blank=True)


    def __str__(self):
        return self.Product

class Nutrient(models.Model):
    NutrientName = models.CharField(max_length=20, null=True, blank=True)
    Nutrient_key = models.CharField(max_length=20, null=True, blank=True)
    Nutrient_unit = models.CharField(max_length=20, null=True, blank=True)
  
    def __str__(self):
        return self.NutrientName




class Diet_sheet(models.Model):
    product_id=models.CharField(max_length=30,primary_key=True)
    product_name=models.CharField(max_length=30, null=True, blank=True)
    Preferrence=models.CharField(max_length=30, null=True, blank=True)
    protein=models.IntegerField(null=True, blank=True)
    carbs=models.IntegerField(null=True, blank=True)
    fat=models.IntegerField(null=True, blank=True)


    def __str__(self):
        return self.product_id


