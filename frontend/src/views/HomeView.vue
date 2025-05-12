<template>
  <div class="bg-white min-h-screen flex flex-col">
    <!-- Hero Section -->
    <section class="text-center py-16 px-4 bg-gradient-to-br from-primary to-secondary text-white">
      <h1 class="text-4xl md:text-5xl font-bold mb-4">Welcome to Bitebooks</h1>
      <p class="text-lg md:text-xl max-w-2xl mx-auto">
        Discover, share, and save your favorite recipes. Your kitchen companion starts here.
      </p>
    </section>

    <!-- Action Buttons -->
    <section class="grid grid-cols-1 md:grid-cols-2 gap-8 px-8 py-16 max-w-5xl mx-auto">
      <!-- Search Recipes -->
      <router-link to="/recipes" class="relative group rounded-2xl overflow-hidden shadow-lg">
        <img src="../assets/search-recipes.jpg" alt="Search Recipes" class="w-full h-80 object-cover transition-transform duration-300 group-hover:scale-105" />
        <div class="absolute inset-0 bg-black/40 group-hover:bg-black/60 transition duration-300"></div>
        <div class="absolute inset-0 flex items-center justify-center">
          <span class="text-white text-2xl font-semibold z-10">Browse Recipes</span>
        </div>
      </router-link>

      <!-- Add a Recipe -->
      <router-link to="/add-recipe" class="relative group rounded-2xl overflow-hidden shadow-lg">
        <img src="../assets/add-recipe.jpg" alt="Add Recipe" class="w-full h-80 object-cover transition-transform duration-300 group-hover:scale-105" />
        <div class="absolute inset-0 bg-black/40 group-hover:bg-black/60 transition duration-300"></div>
        <div class="absolute inset-0 flex items-center justify-center">
          <span class="text-white text-2xl font-semibold z-10">Add Your Recipe</span>
        </div>
      </router-link>
    </section>
  </div>
</template>

<style scoped>
/* You can still use @apply, but scoped styles are minimal here since Tailwind covers it */
</style>
