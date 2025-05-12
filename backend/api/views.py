from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from .models import Recipe, Ingredient, Tag
from .serializers import IngredientSerializer, TagSerializer, RecipeListSerializer, RecipeDetailSerializer, RecipeCreateUpdateSerializer

# Ingredient ViewSet
class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all().order_by('name')
    serializer_class = IngredientSerializer


# Tag ViewSet
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# Recipe ViewSet    
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return RecipeListSerializer
        if self.action == "retrieve":
            return RecipeDetailSerializer
        return RecipeCreateUpdateSerializer

