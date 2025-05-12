from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredient, Tag, RecipeTag

# Ingredient model registration
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Tag model registration
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Recipe model registration
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'servings', 'times_cooked', 'created_at', 'last_cooked_at')
    search_fields = ('name',)
    list_filter = ('tags',)
    readonly_fields = ('times_cooked', 'created_at', 'last_cooked_at')  # Make these fields read-only

    # Add an inline form for RecipeIngredient
    class RecipeIngredientInline(admin.TabularInline):
        model = RecipeIngredient
        extra = 1  # Number of empty ingredient fields to show by default

    class RecipeTagInline(admin.TabularInline):
        model = RecipeTag
        extra = 1

    inlines = [RecipeIngredientInline, RecipeTagInline]

# RecipeIngredient model registration (through model for managing ingredient-quantity relationship)
@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'quantity')
    search_fields = ('ingredient__name',)

# RecipeTag model registration (through model for managing recipe-tags relationship)
@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'tag')
    search_fields = ('tag__name',)
