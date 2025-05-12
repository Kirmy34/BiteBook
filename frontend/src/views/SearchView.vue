<template>
  <div class="p-4 max-w-6xl mx-auto">
    <!-- Hero -->
    <div class="text-center pt-12">
      <h1 class="text-3xl md:text-4xl font-bold mb-2">What are we cooking today?</h1>
      <p class="text-gray-500 text-sm">Search by name, ingredient, or tag</p>
    </div>

    <!-- Search Bar -->
    <div class="flex gap-2 mb-6">
      <input
        v-model="searchQuery"
        @input="filterRecipes"
        type="text"
        placeholder="Search recipes..."
        class="w-full px-4 py-2 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-secondary"
      />
    </div>

    <!-- Tag Filter -->
    <div v-if="allTags.length" class="flex flex-wrap gap-2 mb-6">
      <button
        v-for="tag in allTags"
        :key="tag.id"
        @click="toggleTag(tag)"
        :class="[
          'px-3 py-1 rounded-full text-sm font-medium border',
          activeTagIds.includes(tag.id)
            ? 'bg-secondary text-white border-secondary'
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
        ]"
      >
        {{ tag.name }}
      </button>
    </div>

    <!-- Recipes Grid -->
    <div v-if="filteredRecipes.length" class="grid gap-6 grid-cols-1 sm:grid-cols-2 md:grid-cols-3">
      <router-link
        v-for="recipe in filteredRecipes"
        :key="recipe.id"
        :to="`/recipes/${recipe.id}`"
        class="rounded-xl overflow-hidden shadow hover:shadow-lg transition group"
      >
        <img
          :src="recipe.cover_image || 'images/recipe-placeholder.svg'"
          alt="Recipe Image"
          class="w-full h-48 object-cover group-hover:brightness-75 transition"
        />
        <div class="p-4">
          <h3 class="text-lg font-semibold text-gray-800">{{ recipe.name }}</h3>
          <p class="text-sm text-gray-500 line-clamp-2">{{ recipe.description }}</p>
        </div>
      </router-link>
    </div>

    <!-- Empty State -->
    <p v-else class="text-center text-gray-400 mt-20">No recipes found. Try changing your search or filters.</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getRecipes, getTags } from '@services/api'
import type { Tag } from '@/types'

interface Recipe {
  id: number
  name: string
  cover_image: string
  description: string
  tags: number[]
}

// State
const searchQuery = ref('')
const allRecipes = ref<Recipe[]>([])
const filteredRecipes = ref<Recipe[]>([])
const allTags = ref<Tag[]>([])
const activeTagIds = ref<number[]>([])

// Fetch data
onMounted(async () => {
  const [recipesRes, tagsRes] = await Promise.all([getRecipes(), getTags()])
  allRecipes.value = recipesRes.data
  allTags.value = tagsRes.data
  filterRecipes()
})

// Filter logic
const toggleTag = (tag: Tag) => {
  const index = activeTagIds.value.indexOf(tag.id)
  if (index >= 0) {
    activeTagIds.value.splice(index, 1)
  } else {
    activeTagIds.value.push(tag.id)
  }
  filterRecipes()
}

const filterRecipes = () => {
  const query = searchQuery.value.toLowerCase().trim()

  filteredRecipes.value = allRecipes.value.filter(recipe => {
    const matchesQuery =
      recipe.name.toLowerCase().includes(query) ||
      recipe.description.toLowerCase().includes(query)

    const matchesTags =
      activeTagIds.value.length === 0 ||
      activeTagIds.value.every(tagId => recipe.tags.includes(tagId))

    return matchesQuery && matchesTags
  })
}
</script>

<style scoped>
/* Tailwind handles most of the styling */
</style>
