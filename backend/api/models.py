from datetime import timezone
from django.db import models
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

# Ingredient model
class Ingredient(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.name}"
    
# Tag model
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Recipe model
class Recipe(models.Model):
    name = models.CharField(max_length=50, unique=True)
    cover_image = models.ImageField(upload_to='recipe_covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_cooked_at = models.DateTimeField(blank=True, null=True)
    servings = models.PositiveIntegerField(default=2)
    times_cooked = models.PositiveIntegerField(default=0)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    instructions = models.JSONField(default=list)
    description = models.TextField(blank=True, max_length=100)
    tags = models.ManyToManyField(Tag, through='RecipeTag')

    def save(self, *args, **kwargs):
        # Call save first so we have access to self.cover_image.file
        super().save(*args, **kwargs)

        if self.cover_image:
            img = Image.open(self.cover_image)

            # Convert to RGB (JPEG doesn’t support alpha channel)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Resize the image
            img.thumbnail((800, 800))  # Resize to max 800x800, preserving aspect ratio

            # Save it into a buffer
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=85)
            buffer.seek(0)

            # Replace the image with the processed one
            file_name = f"{self.name.lower().replace(' ', '_')}_cover.jpg"
            self.cover_image.save(file_name, ContentFile(buffer.read()), save=False)

            super().save(update_fields=["cover_image"])

    def increment_times_cooked(self):
        """Increase the times_cooked counter and update last_cooked_at."""
        self.times_cooked += 1
        self.last_cooked_at = timezone.now()
        self.save()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
    


# RecipeIngredient through model
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50)

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f"{self.quantity} of {self.ingredient.name} for {self.recipe.name}"

# RecipeTag through model
class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('recipe', 'tag')

    def __str__(self):
        return f"{self.recipe.name} - {self.tag.name}"
    