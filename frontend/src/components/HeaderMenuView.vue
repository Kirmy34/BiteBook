<template>
  <nav class="bg-primary-dark px-2 flex justify-between w-full header-height">

    <!-- Site Name -->
    <router-link to="/" class="flex items-center space-x-2">
      <img src="../assets/logo_text.png" alt="Logo" class="max-h-16" />
    </router-link>

    <div class="flex items-center">
      <!-- Add Button -->
      <router-link to="/add-recipe">
        <button class="icon-style">
          <Plus class="icon-size text-white" />
        </button>
      </router-link>

      <!-- User Icon -->

      <router-link to="/profile">
        <button class="icon-style">
          <User class="icon-size text-white" />
        </button>
      </router-link>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { User, Plus } from 'lucide-vue-next';
</script>

<style scoped>
@reference "../style.css";

.icon-size {
  @apply h-8 w-8;
}
</style>
