<template>
  <div class="flex flex-col justify-between p-4 content-height w-full max-w-3xl mx-auto">
    <h1 class="text-center mb-6">Step {{ currentStep + 1 }}: {{ steps[currentStep] }}</h1>
    <div class="bg-gray-100 p-4 rounded-lg shadow-md max-h-3/4 overflow-y-auto">

      <!-- Step 1: Recipe Basics -->
      <div v-if="currentStep === 0">
        <!-- Name -->
        <label>Recipe Name</label>
        <input v-model="recipe.name" type="text" class="mt-1 w-full px-4 py-2 border rounded-md" />

        <!-- Description -->
        <label>Description</label>
        <div class="relative">
          <textarea v-model="recipe.description" :maxlength="descriptionMaxLength" rows="3"
            class="mt-1 w-full px-4 py-2 border rounded-md resize-none"></textarea>
          <!-- Character count display -->
          <div class="absolute bottom-2 right-2 text-sm text-gray-500">
            {{ recipe.description.length }} / {{ descriptionMaxLength }}
          </div>
        </div>

        <!-- Servings Input -->
        <label>Servings</label>
        <div class="inline-block mt-1">
          <div class="flex items-center border-1 border-gray-300 rounded-md overflow-hidden">
            <button @click="decreaseServings" class="rounded-r-none ml-1">
              -
            </button>
            <input v-model="recipe.servings" type="number" min="1"
              class="w-16 text-center px-2 rounded-none border-none shadow-none" />
            <button @click="increaseServings" class="rounded-l-none mr-1">
              +
            </button>
          </div>
        </div>

      </div>

      <!-- Step 2: Ingredients -->
      <div v-if="currentStep === 1">

        <!-- Search bar -->
        <input v-model="ingredientSearchQuery" @input="onIngredientSearchQueryChange"
          placeholder="Search for Ingredients" class="w-full mt-4" />


        <!-- Select Ingredients -->
        <div class="flex flex-wrap gap-2 mt-4">
          <!-- Add new Ingredient -->
          <button v-if="ingredientAddingEnabled" @click="createNewIngredient"
            class="button-list-style bg-secondary text-text">
            <Plus class="inline-icon" /> {{ ingredientSearchQuery }}
          </button>

          <!-- Ingredients Search Results -->
          <button v-for="ingredient in displayedIngredients" :key="ingredient.id"
            @click="addIngredientToRecipe(ingredient)" class="button-list-style bg-gray-300 text-text">
            <Carrot class="inline-icon" />{{ ingredient.name }}
          </button>
        </div>

        <!-- Added Ingredients List -->
        <div v-for="(ingredient, index) in RecipeIngredients" :key="index"
          class="flex justify-between items-center gap-2 mt-2 p-2 bg-gray-300 rounded-md">
          <div>
            <h4>
              {{ ingredient.ingredient.name }}
            </h4>
            <input v-model="ingredient.quantity" type="text" placeholder="Quantity" class="inline bg-gray-100" />
          </div>
          <Trash2 @click="RecipeIngredients.splice(index, 1)" class="inline-icon text-red-800" />
        </div>

      </div>

      <!-- Step 3: Instructions -->
      <div v-if="currentStep === 2">
        <label class="block font-medium mb-2">Add step-by-step instructions</label>

        <div class="flex flex-col gap-2">
          <div v-for="(_, index) in recipe.instructions" :key="index" class="flex items-center gap-2">
            <span class="font-bold">{{ index + 1 }}.</span>
            <textarea v-model="recipe.instructions[index]" type="text" placeholder="What to do..." class="w-full"
              cols="2"></textarea>
            <Trash2 @click="removeStep(index)" class="h-6 w-6 text-red-700" />

          </div>
        </div>

        <!-- Add Step Button -->
        <button @click="addStep" class="mt-4 ">
          <Plus class="inline-icon" /> Add Step
        </button>
      </div>

      <!-- Step 4: Tags -->
      <div v-if="currentStep === 3">

        <!-- Selected Tags -->
        <div v-if="selectedTags.length > 0" class="flex flex-wrap gap-2 mt-4">
          <button v-for="tag in selectedTags" :key="tag.id" class="button-list-style">
            <X @click="toggleTag(tag)" class="inline-icon" /> {{ tag.name }}
          </button>
        </div>

        <!-- Search Bar -->
        <!-- <label class="mb-2">Select Tags</label> -->
        <div class="">
          <input type="text" placeholder="Search tags" class="w-full my-2" v-model="tagSearchQuery"
            @input="filterTags" />
          <button v-if="addTag" @click="createNewTag(tagSearchQuery)"
            class="button-list-style bg-secondary text-text mt-4">
            <Plus class="inline-icon" /> {{ tagSearchQuery }}
          </button>
        </div>

        <!-- Tag List -->
        <div v-if="displayedTags.length > 0" class="flex flex-wrap gap-2 mt-4">
          <button v-for="tag in displayedTags" :key="tag.id" @click="toggleTag(tag)"
            class="button-list-style bg-gray-300 text-text">
            <Tag class="inline-icon" /> {{ tag.name }}
          </button>
        </div>
        <div v-else-if="!addTag">
          <p>No Tags to show, how about adding some?</p>
        </div>
      </div>

    </div>
    <!-- End sections -->


    <!-- Step Navigation -->
    <div>
      <!-- Step Indicator -->
      <div class="flex justify-center mt-6">
        <div v-for="(_, index) in steps" :key="index" class="flex items-center mx-2 font-semibold">
          <div :class="['w-8 h-8 flex items-center justify-center rounded-full',
            currentStep === index ? 'bg-primary-dark text-white' : 'bg-gray-300 text-gray-700']"
            @click="currentStep = index">
            {{ index + 1 }}
          </div>
          <span v-if="index < steps.length - 1" class="ml-4">—</span>
        </div>
      </div>

      <!-- Navigation Buttons -->
      <div class="mt-6 flex justify-between items-end">
        <button v-if="currentStep > 0" @click="prevStep" class="button-style">
          Back
        </button>
        <div v-if="currentStep === 0">
        </div>

        <button v-if="currentStep < steps.length - 1" @click="nextStep" class="button-style">
          Next
        </button>

        <button v-if="currentStep === steps.length - 1" @click="submitRecipe" class="button-style">
          Submit Recipe
        </button>
      </div>
    </div>
  </div>

</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { Trash2, Plus, Tag, X, Carrot } from 'lucide-vue-next';
import { getIngredients, createIngredient, getTags, createTag, createRecipe } from "../services/api";
import { useToast } from 'vue-toastification';

const toast = useToast();



onMounted(async () => {

  // Get Ingredients
  try {
    const response = await getIngredients();
    availableIngredients.value = response.data;
  } catch (error) {
    toast.error("Error fetching ingredients")
    console.error('Error fetching ingredients:', error);
  }

  // Get Tags
  try {
    const response = await getTags();
    availableTags.value = response.data;
    displayedTags.value = response.data;
  } catch (error) {
    console.error('Error fetching tags:', error);
  }
});

// Main Structs
interface Ingredient {
  id: number;
  name: string;
}

interface RecipeIngredient {
  ingredient: Ingredient;
  quantity: string;
}

interface Tag {
  id: number;
  name: string;
}

// ===== Navigation methods =====
const currentStep = ref(0);
const steps = ['Basics', 'Ingredients', 'Instructions', 'Tags'];

const nextStep = () => {
  if (currentStep.value < steps.length - 1) currentStep.value++;
};

const prevStep = () => {
  if (currentStep.value > 0) currentStep.value--;
};


// ===== Basics Section =====
const recipe = ref({
  name: '',
  description: '',
  servings: 4,
  ingredients: [{ id: '', quantity: '' }],
  instructions: [''],
  tags: []
});

const descriptionMaxLength = 100;  // Set maximum character limit for description

const increaseServings = () => {
  recipe.value.servings++;
};

const decreaseServings = () => {
  if (recipe.value.servings > 1) {
    recipe.value.servings--;
  }
};

// ===== Ingredient Section =====
const displayedIngredients = ref<Ingredient[]>([]);
const availableIngredients = ref<Ingredient[]>([]);
const RecipeIngredients = ref<RecipeIngredient[]>([]);

const ingredientAddingEnabled = ref(false);

const ingredientSearchQuery = ref('');


const onIngredientSearchQueryChange = () => {
  checkAddIngredient();

  if (ingredientSearchQuery.value.length < 2) {
    displayedIngredients.value = [];
    return;
  }

  displayedIngredients.value = availableIngredients.value.filter(ingredient => ingredient.name.toLowerCase().includes(ingredientSearchQuery.value.toLowerCase()));
};

const createNewIngredient = () => {
  createIngredient(ingredientSearchQuery.value).then(response => {
    const newIngredient = response.data;
    availableIngredients.value.push(newIngredient);
    addIngredientToRecipe(newIngredient);
  }).catch(error => {
    console.error('Error creating ingredient:', error);
  });
};

const addIngredientToRecipe = (ingredient: Ingredient) => {
  RecipeIngredients.value.unshift({ ingredient, quantity: '' });
  ingredientSearchQuery.value = '';
  onIngredientSearchQueryChange();
};

const checkAddIngredient = () => {
  ingredientAddingEnabled.value = false;

  // New ingredient name too short
  if (ingredientSearchQuery.value.length < 2) {
    return;
  }

  // Ingredient already exists
  if (availableIngredients.value.some(ingredient => ingredient.name.toLowerCase() === ingredientSearchQuery.value.toLowerCase())) {
    return;
  }

  // Allow adding new ingredient
  ingredientAddingEnabled.value = true;

};


// ===== Instructions Section =====


// Add new instruction step
const addStep = () => {
  recipe.value.instructions.push('');
};

// Remove an instruction step
const removeStep = (stepIndex: number) => {
  if (recipe.value.instructions.length > 1) {
    recipe.value.instructions.splice(stepIndex, 1);
  }
};



// ===== Tags Section =====
const availableTags = ref<Tag[]>([]);
const searchTags = ref<Tag[]>([]);
const selectedTags = ref<Tag[]>([]);
const displayedTags = ref<Tag[]>([]);
const addTag = ref(false);

const tagSearchQuery = ref('');

const toggleTag = (tag: Tag): void => {
  if (selectedTags.value.some(t => t.id === tag.id)) {
    selectedTags.value = selectedTags.value.filter(t => t.id !== tag.id);
  } else {
    selectedTags.value.push(tag);
  }
  updateDisplayedTags();
};

const filterTags = (): void => {
  if (tagSearchQuery.value.length < 2) {
    searchTags.value = availableTags.value;
    addTag.value = false;
  } else {
    searchTags.value = availableTags.value.filter(tag => tag.name.toLowerCase().includes(tagSearchQuery.value.toLowerCase()));
    if (searchTags.value.length === 0) {
      addTag.value = true;
    } else {
      addTag.value = false;
    }
  }
  updateDisplayedTags();
};

const updateDisplayedTags = (): void => {
  displayedTags.value = searchTags.value.filter(tag => !selectedTags.value.find(selectedTag => selectedTag.id === tag.id));
};

const createNewTag = (name: string): void => {
  createTag(name).then(response => {
    const newTag = response.data;
    availableTags.value.push(newTag);
    selectedTags.value.push(newTag);
    tagSearchQuery.value = '';
    addTag.value = false;
    updateDisplayedTags();
  }).catch(error => {
    console.error('Error creating tag:', error);
  });
};

// ===== Submit Section =====

const validateRecipeData = () => {

  let isValid = true;

  // Check if the recipe has a name and description
  if (!recipe.value.name) {
    toast.error('Please provide a name for the recipe.');
    isValid = false;
  }

  // Check if the recipe has ingredients
  if (recipe.value.ingredients.length === 0) {
    toast.error('Please add at least one ingredient.');
    isValid = false;
  }

  // Check if instructions are provided
  if (recipe.value.instructions.length === 0 || recipe.value.instructions.some(step => !step.trim())) {
    toast.error('Please provide recipe instructions.');
    isValid = false;
  }

  return isValid;
};


// Submit Recipe
const submitRecipe = async () => {


  console.log(RecipeIngredients.value);

  // Validate the recipe data
  if (!validateRecipeData()) return;


  // Prepare the recipe data to be sent to the API
  const recipeData = {
    name: recipe.value.name,
    description: recipe.value.description,
    servings: recipe.value.servings,
    ingredients: RecipeIngredients.value.map(({ ingredient, quantity }) => ({
      id: ingredient.id,
      quantity
    })),
    instructions: recipe.value.instructions,
    tags: selectedTags.value.map(tag => tag.id),
  };

  console.log(recipeData);


  try {
    await createRecipe(recipeData);
    
    toast.success('Recipe submitted successfully!');


  } catch (error) {
    console.log(error);
    toast.error('Error submitting recipe.');
  }
};

</script>

<style scoped>
@reference "../style.css";

.button-list-style {
  @apply rounded-full px-2 py-1 flex items-center
}

.inline-icon {
  @apply h-4 w-4 mr-1 inline;
}
</style>
