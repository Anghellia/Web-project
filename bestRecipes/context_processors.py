from .models import Recipe
from collections import Counter


dif_choices = (
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Profi', 'Profi')
)

def get_cat_list(recipe):
    return recipe.categories.split(',')

def categories(request):
    all_recipes = Recipe.objects.all()
    cat_list = Counter([cat for recipe in all_recipes for cat in get_cat_list(recipe)])
    sorted_cat = dict(sorted(cat_list.items(), key=lambda x: x[1], reverse=True))
    return {'categories': sorted_cat}
