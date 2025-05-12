<template>
  <div class="flex flex-col justify-between p-4 content-height w-full max-w-3xl mx-auto">
    <h1 class="text-center mb-6">Step {{ currentStep + 1 }}: {{ steps[currentStep].label }}</h1>

    <!-- Dynamic Step Component -->
    <component :is="steps[currentStep].component"
               v-bind="steps[currentStep].props"
               @update="handleStepUpdate"
               class="bg-gray-100 p-4 rounded-lg shadow-md min-h-1/4 max-h-3/4 overflow-y-auto" />

    <!-- Navigation -->
    <div>
      <!-- Step Indicators -->
      <div class="flex justify-center mt-6">
        <div v-for="(_, index) in steps"
             :key="index"
             class="flex items-center mx-2 font-semibold">
          <div :class="[
            'w-8 h-8 flex items-center justify-center rounded-full cursor-pointer',
            currentStep === index ? 'bg-primary-dark text-white' : 'bg-gray-300 text-gray-700'
          ]"
               @click="currentStep = index">
            {{ index + 1 }}
          </div>
          <span v-if="index < steps.length - 1"
                class="ml-4">—</span>
        </div>
      </div>

      <!-- Buttons -->
      <div class="mt-6 flex justify-between items-end">
        <button v-if="currentStep > 0"
                @click="currentStep--"
                class="button-style">Back</button>
        <div v-else></div> <!-- Empty div for alignment -->
        <button v-if="currentStep < steps.length - 1"
                @click="currentStep++"
                class="button-style">
          Next
        </button>
        <button v-if="currentStep === steps.length - 1"
                @click="submitRecipe"
                class="button-style">
          Submit Recipe
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import { useToast } from 'vue-toastification';
import { createRecipe } from '@services/api';
import type { RecipeIngredientType, TagType } from '@/types';

import RecipeStepBasics from '@/components/RecipeSteps/RecipeStepBasics.vue';
import RecipeStepIngredients from '@/components/RecipeSteps/RecipeStepIngredients.vue';
import RecipeStepInstructions from '@/components/RecipeSteps/RecipeStepInstructions.vue';
import RecipeStepTags from '@/components/RecipeSteps/RecipeStepTags.vue';

const toast = useToast();

// Group recipe data
const recipe = reactive({
  name: '',
  description: '',
  servings: 4,
  ingredients: [] as RecipeIngredientType[],
  instructions: [] as string[],
  tags: [] as TagType[]
});

// Step control
const currentStep = ref(0);

// Define step metadata
const steps = computed(() => [
  {
    label: 'Basics',
    component: RecipeStepBasics,
    props: {
      initialName: recipe.name,
      initialDescription: recipe.description,
      initialServings: recipe.servings
    }
  },
  {
    label: 'Ingredients',
    component: RecipeStepIngredients,
    props: {
      initialIngredients: recipe.ingredients
    }
  },
  {
    label: 'Instructions',
    component: RecipeStepInstructions,
    props: {
      initialInstructions: recipe.instructions
    }
  },
  {
    label: 'Tags',
    component: RecipeStepTags,
    props: {
      initialTags: recipe.tags
    }
  }
]);

// Unified event handler
function handleStepUpdate(payload: Partial<typeof recipe>) {
  Object.assign(recipe, payload);
}

// Submit & validate
function validateRecipeData() {
  const { name, ingredients, instructions } = recipe;
  if (!name) return toast.error('Please provide a name for the recipe.'), false;
  if (!ingredients.length) return toast.error('Please add at least one ingredient.'), false;
  if (!instructions.length || instructions.some(step => !step.trim()))
    return toast.error('Please provide recipe instructions.'), false;
  return true;
}

async function submitRecipe() {
  if (!validateRecipeData()) return;

  try {
    await createRecipe({
      name: recipe.name,
      description: recipe.description,
      servings: recipe.servings,
      instructions: recipe.instructions,
      ingredients: recipe.ingredients.map(i => ({
        id: i.ingredient.id,
        quantity: i.quantity
      })),
      tags: recipe.tags.map(t => t.id)
    });

    toast.success('Recipe submitted successfully!');
    // Reset if you want
    // Object.assign(recipe.value, { name: '', description: '', servings: 4, ingredients: [], instructions: [], tags: [] });
    // currentStep.value = 0;
  } catch (err) {
    toast.error('Error submitting recipe.');
    console.error(err);
  }
}
</script>

<style scoped>
@import '../style.css';
</style>
