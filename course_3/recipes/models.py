import pint
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from .utils import number_str_to_float
from django.contrib.auth.models import User
from .validators import validate_unit_of_measure

class Recipe(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="recipes"
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    directions = models.TextField(help_text="Step-by-step cooking instructions")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def get_ingredients_children(self):
        print(self.ingredients.all())
        return self.ingredients.all() 
    
    def get_hx_url(self):
        return reverse("recipe-detail", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        "Recipe", 
        on_delete=models.CASCADE, 
        related_name="ingredients"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    unit = models.CharField(max_length=50, validators=[validate_unit_of_measure]) 
    quantity = models.CharField(max_length=50)   
    quantity_as_float = models.FloatField(blank=True, null=True)   

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"
    
    def get_hx_edit_url(self):
        kwargs={
            "slug": self.recipe.slug,
            "id": self.id,
        }
        return reverse("recipe-ingredient-update-hx", kwargs=kwargs)
    
    def convert_to_system(self, system="mks"):
        if self.quantity_as_float is None:
            return None
        ureg = pint.UnitRegistry(system=system)
        measurement = self.quantity_as_float * ureg[self.unit]
        return measurement
    
    def as_mks(self):
        return self.convert_to_system("mks").to_base_units()
    
    def as_imperial(self):
        return self.convert_to_system("imperial").to_base_units()

    def save(self, *args, **kwargs):
        qty = self.quantity
        qty_as_float, qty_as_float_success = number_str_to_float(qty)
        if qty_as_float_success:
            self.quantity_as_float = qty_as_float
        else:
            self.quantity_as_float = None
        super().save(*args, **kwargs)
