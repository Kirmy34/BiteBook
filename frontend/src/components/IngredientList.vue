<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getIngredients, addIngredient, deleteIngredient, updateIngredient } from "../services/api";
import { PencilIcon, TrashIcon, CheckIcon, PlusIcon } from '@heroicons/vue/24/solid'; // Import the icons

interface Ingredient {
  id: number;
  name: string;
}

const ingredients = ref<Ingredient[]>([]);
const newIngredient = ref("");
const editingIngredientId = ref<number | null>(null);
const editedName = ref("");

const fetchIngredients = async () => {
  try {
    const response = await getIngredients();
    ingredients.value = response.data;
  } catch (error) {
    console.error("Error fetching ingredients:", error);
  }
};

const createIngredient = async () => {
  if (!newIngredient.value.trim()) return; // Prevent empty submissions
  try {
    const response = await addIngredient(newIngredient.value);
    ingredients.value.push(response.data); // Add new ingredient to list
    newIngredient.value = ""; // Clear input field
  } catch (error) {
    console.error("Error adding ingredient:", error);
  }
};

const removeIngredient = async (id: number) => {
  try {
    await deleteIngredient(id);
    ingredients.value = ingredients.value.filter((ingredient) => ingredient.id !== id);
  } catch (error) {
    console.error("Error deleting ingredient:", error);
  }
};

const startEditing = (ingredient: Ingredient) => {
  editingIngredientId.value = ingredient.id;
  editedName.value = ingredient.name;
};

const saveEdit = async () => {
  if (editedName.value.trim() === "") return;
  try {
    await updateIngredient(editingIngredientId.value!, editedName.value);
    const updatedIngredient = ingredients.value.find(
      (ingredient) => ingredient.id === editingIngredientId.value
    );
    if (updatedIngredient) {
      updatedIngredient.name = editedName.value; // Update the name locally
    }
    editingIngredientId.value = null; // Reset the editing state
    editedName.value = ""; // Clear the edited name
  } catch (error) {
    console.error("Error updating ingredient:", error);
  }
};

onMounted(fetchIngredients);
</script>

<template>
  <div class="p-4 w-md mx-auto bg-gray-200 rounded-md">
    <h2 class="text-2xl font-semibold text-gray-700 mb-4">Ingredients</h2>

    <!-- Ingredient List -->
    <ul v-if="ingredients.length" class="space-y-2">
      <li
        v-for="ingredient in ingredients"
        :key="ingredient.id"
        class="flex justify-between items-center p-2 bg-gray-100 rounded-md shadow-sm"
      >
        <span v-if="editingIngredientId !== ingredient.id" class="text-gray-700">
          {{ ingredient.name }}
        </span>
        <input
          v-else
          v-model="editedName"
          class="text-gray-700 p-2 rounded-md border-2 border-gray-300 w-full"
        />
        <div class="space-x-2 flex items-center">
          <button
            v-if="editingIngredientId !== ingredient.id"
            @click="startEditing(ingredient)"
            class="bg-yellow-500 text-white p-2 rounded-md hover:bg-yellow-600 transition duration-200"
          >
            <PencilIcon class="h-5 w-5" />
          </button>
          <button
            v-else
            @click="saveEdit"
            class="bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600 transition duration-200"
          >
            <CheckIcon class="h-5 w-5" />
          </button>
          <button
            @click="removeIngredient(ingredient.id)"
            class="bg-red-500 text-white p-2 rounded-md hover:bg-red-600 transition duration-200"
          >
            <TrashIcon class="h-5 w-5" />
          </button>
        </div>
      </li>
    </ul>
    
    <p v-else class="text-gray-500">Loading ingredients...</p>

    
    <!-- Add Ingredient Form -->
    <form @submit.prevent="createIngredient" class="mt-4 flex space-x-2">
      <input
        v-model="newIngredient"
        type="text"
        placeholder="Enter ingredient name"
        class="border-2 border-gray-300 p-2 rounded-md w-full"
        required
      />
      <button
        type="submit"
        class="bg-green-500 text-white p-2 rounded-md hover:bg-green-600 transition duration-200"
      >
      <PlusIcon class="h-5 w-5" />
      </button>
    </form>

  </div>
</template>

<style scoped>
/* You can add any custom styles here if needed */
</style>
