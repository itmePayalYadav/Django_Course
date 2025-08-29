from django.test import TestCase
from .models import RecipeIngredient, Recipe
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class UserTestCase(TestCase):
    def setUp(self):
        self.user_a =  User.objects.create_user('test', password='test@123')

    def test_user_pw(self):
        checked = self.user_a.check_password("test@123")
        self.assertTrue(checked)

class RecipeTest(TestCase):
    def setUp(self):
        self.user_a =  User.objects.create_user('test', password='test@123')
        self.recipe_a = Recipe.objects.create(
            user=self.user_a,
            name="test recipe"
        )
        self.recipe_ingredient_a =  RecipeIngredient.objects.create(
            recipe=self.recipe_a,
            name="test recipe ingredient",
            quantity="100",
            unit="gm"
        ) 
        self.recipe_ingredient_b =  RecipeIngredient.objects.create(
            recipe=self.recipe_a,
            name="test recipe ingredient",
            quantity="smdsdnasjda",
            unit="gm"
        )     

    def test_user_count(self):
        qs = User.objects.all()
        self.assertEqual(qs.count(), 1)
    
    def test_user_recipe_reverse_count(self):
        user = self.user_a
        qs = user.recipes.all()
        self.assertEqual(qs.count(), 1)

    def test_user_recipe_forward_count(self):
        user = self.user_a
        qs = Recipe.objects.filter(user=user)
        self.assertEqual(qs.count(), 1)

    def test_recipe_ingridient_reverse_count(self):
        recipe = self.recipe_a
        qs = recipe.ingredients.all()
        self.assertEqual(qs.count(), 2)

    def test_recipe_ingridient_count(self):
        recipe = self.recipe_a
        qs = RecipeIngredient.objects.filter(recipe=recipe)
        self.assertEqual(qs.count(), 2)

    def test_user_two_level_relation(self):
        user = self.user_a
        qs = RecipeIngredient.objects.filter(recipe__user=user)
        self.assertEqual(qs.count(), 2)

    def test_user_two_level_relation_reverse(self):
        user = self.user_a
        ri_ids = list(user.recipes.all().values_list('ingredients__id', flat=True))
        qs = RecipeIngredient.objects.filter(id__in=ri_ids)
        self.assertEqual(qs.count(), 2)
    
    def test_user_two_level_relation_via_recipes(self):
        user = self.user_a
        ids = user.recipes.all().values_list('id', flat=True)
        qs = RecipeIngredient.objects.filter(recipe__id__in=ids)
        self.assertEqual(qs.count(), 2)
        
    def test_unit_measure_validation_error(self):
        invalid_unit = 'ounce'
        ingridient = RecipeIngredient(
            name='New',
            quantity=10,
            recipe=self.recipe_a,
            unit=invalid_unit
        )
        ingridient.full_clean()

    def test_unit_measure_validation_error_invalid(self):
        invalid_unit = 'nada'
        with self.assertRaises(ValidationError):
            ingridient = RecipeIngredient(
                name='New',
                quantity=10,
                recipe=self.recipe_a,
                unit=invalid_unit
            )
            ingridient.full_clean()

    def test_quantity_as_float(self):
        self.assertIsNotNone(self.recipe_ingredient_a.quantity_as_float)
        self.assertIsNone(self.recipe_ingredient_b.quantity_as_float)
    
    