<template>
  <div>
    <h2 class="text-xl font-semibold">Recipe Basics</h2>

    <!-- Recipe Name -->
    <label for="recipeName"
           class="block mt-4">Recipe Name</label>
    <input id="recipeName"
           v-model="localName"
           type="text"
           class="w-full px-4 py-2 border rounded-md"
           placeholder="Enter recipe name" />

    <!-- Recipe Description -->
    <label for="recipeDescription"
           class="block mt-4">Description</label>
    <div class="relative">
      <textarea id="recipeDescription"
                v-model="localDescription"
                :maxlength="descriptionMaxLength"
                rows="3"
                class="w-full px-4 py-2 border rounded-md resize-none"
                placeholder="Enter recipe description"></textarea>
      <div class="absolute bottom-1 right-2 text-sm text-gray-500">
        {{ localDescription.length }} / {{ descriptionMaxLength }}
      </div>
    </div>

    <!-- Servings Input -->
    <label class="block mt-4">Servings</label>
    <div class="inline-flex items-center border border-gray-300 rounded-md overflow-hidden">
      <button @click="decreaseServings"
              class="px-2">-</button>
      <input v-model.number="localServings"
             type="number"
             min="1"
             class="w-16 text-center border-l border-r border-gray-200" />
      <button @click="increaseServings"
              class="px-2">+</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, watchEffect, defineProps, defineEmits } from 'vue';

const props = defineProps<{
  initialName?: string;
  initialDescription?: string;
  initialServings?: number;
}>();

const emit = defineEmits<{
  (event: 'update', payload: {
    name: string;
    description: string;
    servings: number;
  }): void;
}>();

const localName = ref(props.initialName ?? '');
const localDescription = ref(props.initialDescription ?? '');
const localServings = ref(props.initialServings ?? 1);

const descriptionMaxLength = 100;

// Emit on change
watchEffect(() => {
  emit('update', {
    name: localName.value,
    description: localDescription.value,
    servings: localServings.value,
  });
});

// Ensure servings is at least 1
watch(localServings, (val) => {
  if (val < 1) localServings.value = 1;
});

// Servings handlers
const increaseServings = () => localServings.value++;
const decreaseServings = () => {
  if (localServings.value > 1) localServings.value--;
};
</script>
