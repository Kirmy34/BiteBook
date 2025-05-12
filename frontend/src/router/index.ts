import { createRouter, createWebHistory } from "vue-router";
import SearchView from "@views/SearchView.vue";
import RecipeForm from "@views/RecipeForm.vue";
import RecipeDetails from "@views/RecipeDetails.vue";
import NotFoundView from "@views/NotFoundView.vue"; // 404 Page

const routes = [
  { path: "/", component: SearchView, name: "Home" },
  { path: "/add-recipe", component: RecipeForm, name: "AddRecipe" },
  { path: '/recipes/:id', component: RecipeDetails, name: 'RecipeDetails' },
  { path: "/:pathMatch(.*)*", component: NotFoundView, name: "NotFound" }, // Catch-all route for 404
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
