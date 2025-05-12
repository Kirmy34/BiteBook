import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getIngredients = () => api.get("/ingredients/");
export const createIngredient = (name: string) => api.post("/ingredients/", { name });
export const getTags = () => api.get("/tags/");
export const createTag = (name: string) => api.post("/tags/", { name });
export const createRecipe = (recipe: any) => api.post("/recipes/", recipe);
export const getRecipeById = (id: string) => api.get(`/recipes/${id}/`);
export const getRecipes = () => api.get("/recipes/");

export default api;
