<template>
  <div v-if="recipe"
       class="max-w-4xl mx-auto p-6">
    <!-- Cover Image -->
    <div class="mb-6 rounded-xl overflow-hidden shadow">
      <img :src="recipe.cover_image || '/images/recipe-placeholder.svg'"
           alt="Recipe Cover"
           class="w-full h-64 object-cover" />
    </div>

    <!-- Upload input -->
    <div class="absolute bottom-2 right-2">
      <input type="file"
             accept="image/*"
             @change="onImageSelected"
             class=""
             ref="fileInput" />
      <button @click="() => fileInput?.click()"
              class="bg-white text-black text-sm px-4 py-2 rounded shadow">
        Change Cover
      </button>
    </div>

    <!-- Upload Button -->
    <div v-if="selectedImage"
         class="mb-6">
      <button @click="uploadImage"
              class="bg-primary-dark text-white px-4 py-2 rounded">
        Upload Image
      </button>
    </div>

    <!-- Title + Description -->
    <div class="mb-6">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ recipe.name }}</h1>
      <p class="text-gray-700 text-lg">{{ recipe.description }}</p>
    </div>

    <!-- Tags -->
    <div v-if="recipe.tags.length"
         class="mb-6 flex flex-wrap gap-2">
      <span v-for="tag in recipe.tags"
            :key="tag.id"
            class="bg-secondary text-text text-sm px-3 py-1 rounded-full">
        {{ tag.name }}
      </span>
    </div>

    <!-- Info Section -->
    <div class="flex items-center gap-4 mb-6 text-sm text-gray-600">
      <div>🍽 Servings: {{ recipe.servings }}</div>
    </div>

    <!-- Ingredients -->
    <div class="mb-8">
      <h2 class="text-xl font-semibold text-gray-800 mb-3">Ingredients</h2>
      <ul class="list-disc pl-5 space-y-1">
        <li v-for="(item, index) in recipe.ingredients"
            :key="index">
          {{ item.quantity }} of {{ item.name }}
        </li>
      </ul>
    </div>

    <!-- Instructions -->
    <div>
      <h2 class="text-xl font-semibold text-gray-800 mb-3">Instructions</h2>
      <ol class="list-decimal pl-5 space-y-3">
        <li v-for="(step, index) in recipe.instructions"
            :key="index">
          {{ step }}
        </li>
      </ol>
    </div>
  </div>

  <!-- Optional Loading State -->
  <div v-else
       class="text-center mt-10 text-gray-500">Loading recipe...</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { getRecipeById } from '@/services/api';
import axios from 'axios';

const route = useRoute();
const recipeId = route.params.id as string;
const selectedImage = ref<File | null>(null);
const previewImage = ref<string | null>(null);
const fileInput = ref<HTMLInputElement | null>(null);

const recipe = ref<null | {
  id: number
  name: string;
  description: string;
  cover_image?: string;
  servings: number;
  tags: { id: number; name: string }[];
  ingredients: { name: string; quantity: string }[];
  instructions: string[];
}>(null);


const onImageSelected = (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (file) {
    selectedImage.value = file;
    previewImage.value = URL.createObjectURL(file);
  }
};

const uploadImage = async () => {
  if (!selectedImage.value || !recipe.value?.id) return;

  const formData = new FormData();
  formData.append('cover_image', selectedImage.value);

  try {
    await axios.patch(`/api/recipes/${recipe.value.id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    selectedImage.value = null;
    previewImage.value = null;
    await getRecipeById(recipeId); // Refresh data with updated image
  } catch (error) {
    console.error('Image upload failed:', error);
  }
};




onMounted(async () => {
  try {
    const response = await getRecipeById(recipeId);
    recipe.value = response.data;
  } catch (error) {
    console.error('Failed to load recipe:', error);
  }
});
</script>
