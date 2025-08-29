from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Recipe, RecipeIngredient

User = get_user_model()

class RecipeInline(admin.StackedInline):
    model = Recipe
    extra = 0

class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 0
    readonly_fields = ['quantity_as_float', 'as_mks', 'as_imperial']
    
class UserAdmin(admin.ModelAdmin):
    inlines = [RecipeInline]  
    list_display = ['username', 'email', 'is_staff']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ['id', 'name', 'user', 'created_at', 'updated_at', 'active']
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['name', 'description', 'directions']
    raw_id_fields = ['user']
    list_filter = ['active', 'created_at']  

admin.site.register(Recipe, RecipeAdmin)
