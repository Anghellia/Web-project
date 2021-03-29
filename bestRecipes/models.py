from django.db.models import *
from django.contrib.auth.models import User
from pytils.translit import slugify


dif_choices = (
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Profi', 'Profi')
)

def generate_slug(model, title):
    origin_slug = slugify(title)
    unique_slug = origin_slug
    i = 1
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{origin_slug}-{i}"
        i += 1
    return unique_slug


class Recipe(Model):
    title = CharField(max_length=80)
    author = ForeignKey(User, on_delete=CASCADE, default=1)
    created_at = DateTimeField('creation timestamp', auto_now_add=True)
    updated_at = DateTimeField('update timestamp', auto_now=True)
    categories = CharField(max_length=120)
    difficulty = CharField(max_length=20, choices=dif_choices)
    cooking_time = PositiveIntegerField()
    image = ImageField(upload_to='images/')
    slug = SlugField(unique=True, blank=True, default=1)
    text = TextField(max_length=4096)

    def __str__(self):
        return str(self.title)

    def get_categories(self):
        return self.categories.split(',')

    def save(self, *args, **kwargs):
        self.slug = generate_slug(Recipe, self.title)
        super().save(*args, **kwargs)


class Comment(Model):
    author = ForeignKey(User, on_delete=CASCADE)
    recipe = ForeignKey(Recipe, on_delete=CASCADE, related_name='comments')
    text = TextField(max_length=1000)
    created_at = DateTimeField('creation timestamp', auto_now_add=True)

    def __str__(self):
        return str(self.text)
