from rest_framework import serializers
from .models import Tag, Ingredient, Recipe, RecipeIngredient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class IngredientInlineSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'quantity']

    def get_quantity(self, obj):
        return self.context['quantities'].get(obj.id, None)

# Serializer for detailed recipe retrieval
class RecipeDetailSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    instructions = serializers.JSONField()

    class Meta:
        model = Recipe
        fields = ["id", "name", "cover_image", "description", "servings", "instructions", "ingredients", "tags"]

    def get_ingredients(self, obj):
        # Get all RecipeIngredient instances
        recipe_ingredients = obj.recipeingredient_set.select_related('ingredient')
        
        # Build a map of quantities per ingredient ID
        quantities = {ri.ingredient.id: ri.quantity for ri in recipe_ingredients}

        # Get the ingredients queryset
        ingredients = [ri.ingredient for ri in recipe_ingredients]

        # Serialize using IngredientInlineSerializer with extra context for quantity
        serializer = IngredientInlineSerializer(ingredients, many=True, context={'quantities': quantities})
        return serializer.data

# Serializer for listing all recipes
class RecipeListSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    def get_tags(self, obj):
        return list(obj.tags.values_list("id", flat=True))


    class Meta:
        model = Recipe
        fields = ["id", "name", "cover_image", "description", "tags"]


# Serializer for creating and updating recipes
class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    ingredients = serializers.ListField(child=serializers.DictField(), write_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    def get_tags(self, obj):
       return list(obj.tags.values_list("id", flat=True))


    class Meta:
        model = Recipe
        fields = ["name", "cover_image", "description", "servings", "instructions", "ingredients", "tags"]

    def create(self, validated_data):
        ingredients_data = validated_data.pop("ingredients", [])
        tags_data = validated_data.pop("tags", [])

        recipe = Recipe.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get("id")
            quantity = ingredient_data.get("quantity")
            ingredient = Ingredient.objects.get(id=ingredient_id)
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, quantity=quantity)

        recipe.tags.set(tags_data)

        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop("ingredients", [])
        tags_data = validated_data.pop("tags", [])

        instance.name = validated_data.get("name", instance.name)
        instance.cover_image = validated_data.get("cover_image", instance.cover_image)
        instance.description = validated_data.get("description", instance.description)
        instance.servings = validated_data.get("servings", instance.servings)
        instance.instructions = validated_data.get("instructions", instance.instructions)
        instance.save()

        # Update ingredients
        instance.recipeingredient_set.all().delete()  # Remove old ingredients
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get("id")
            quantity = ingredient_data.get("quantity")
            ingredient = Ingredient.objects.get(id=ingredient_id)
            RecipeIngredient.objects.create(recipe=instance, ingredient=ingredient, quantity=quantity)

        # Update tags
        instance.tags.set(tags_data)

        return instance
