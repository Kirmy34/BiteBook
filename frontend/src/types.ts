export interface IngredientType {
  id: number;
  name: string;
}

export interface RecipeIngredientType {
  ingredient: IngredientType;
  quantity: string;
}

export interface TagType {
  id: number;
  name: string;
}
