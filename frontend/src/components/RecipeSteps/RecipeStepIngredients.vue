<template>
  <div>
    <h2 class="text-xl font-semibold">Recipe Ingredients</h2>

    <!-- Ingredient Search Input -->
    <input v-model="searchQuery"
           type="text"
           placeholder="Search for Ingredients"
           class="w-full mt-4 px-4 py-2 border rounded-md" />

    <!-- New Ingredient Button -->
    <button v-if="addingEnabled"
            @click="createNewIngredient"
            class="button-list-style bg-secondary text-text mt-4">
      <Plus class="inline-icon" /> {{ searchQuery }}
    </button>

    <!-- Ingredients Search Results -->
    <div class="flex flex-wrap gap-2 mt-4">
      <button v-for="ingredient in displayedIngs"
              :key="ingredient.id"
              @click="addIngredientToRecipe(ingredient)"
              class="button-list-style bg-gray-300 text-text">
        <Carrot class="inline-icon" /> {{ ingredient.name }}
      </button>
    </div>

    <!-- Added Ingredients List -->
    <div v-for="(ingredient, index) in localIngs"
         :key="index"
         class="flex justify-between items-center gap-2 mt-2 p-2 bg-gray-300 rounded-md">
      <div>
        <h4>{{ ingredient.ingredient.name }}</h4>
        <input v-model="ingredient.quantity"
               type="text"
               placeholder="Quantity"
               class="inline bg-gray-100" />
      </div>
      <Trash2 @click="removeIngredient(index)"
              class="inline-icon text-red-800" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits, watch, computed, onMounted } from 'vue';
import { Plus, Carrot, Trash2 } from 'lucide-vue-next';
import { createIngredient, getIngredients } from '@services/api';
import type { RecipeIngredientType, IngredientType } from '@/types';

// Props to accept initial ingredients list
const props = defineProps<{
  initialIngredients?: RecipeIngredientType[];
}>();

// Local state for ingredients
const localIngs = ref<RecipeIngredientType[]>(props.initialIngredients as RecipeIngredientType[] ?? []);
const displayedIngs = ref<IngredientType[]>([]);
const availableIngs = ref<IngredientType[]>([]);
const addingEnabled = ref(false);
const searchQuery = ref("");

// Filtered ingredients based on search query
const matchingIngredients = computed(() =>
  availableIngs.value.filter(ingredient =>
    ingredient.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
);

const emit = defineEmits<{
  (event: 'update',
    payload: { ingredients: Array<RecipeIngredientType> }): void;
}>();

watch(localIngs, () => {
  emit('update', { ingredients: [...localIngs.value] });
});

// Watch for changes in the search query and update displayed ingredients
watch(searchQuery, () => {
  displayedIngs.value = searchQuery.value.length >= 2
    ? matchingIngredients.value
    : [];

  const exactMatch = availableIngs.value.some(
    i => i.name.toLowerCase() === searchQuery.value.toLowerCase()
  );
  addingEnabled.value = searchQuery.value.length >= 2 && !exactMatch;
});

// Add ingredient to the recipe
const addIngredientToRecipe = (ingredient: IngredientType) => {
  localIngs.value.push({ ingredient, quantity: '' });
  searchQuery.value = '';
};

// Remove ingredient from the list
const removeIngredient = (index: number) => {
  localIngs.value.splice(index, 1);
};

// Create a new ingredient if not available
const createNewIngredient = async () => {
  try {
    const normalizedName = searchQuery.value.trim().replace(/\s+/g, ' ');
    const capitalized = normalizedName.charAt(0).toUpperCase() + normalizedName.slice(1);
    const response = await createIngredient(capitalized);
    const newIngredient = response.data;
    availableIngs.value.push(newIngredient);
    addIngredientToRecipe(newIngredient);
  } catch (error) {
    console.error('Error creating ingredient:', error);
  }
};

// Lifecycle: init
onMounted(async () => {

  // Fetch available ingredients
  try {
    const response = await getIngredients();
    availableIngs.value = response.data;
  } catch (error) {
    console.error('Error fetching ingredients:', error);
  }
});

</script>
