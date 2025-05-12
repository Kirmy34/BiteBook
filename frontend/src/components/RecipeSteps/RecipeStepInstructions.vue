<template>
    <div>
        <h2 class="text-xl font-semibold mb-4">Recipe Instructions</h2>

        <div v-for="(_, index) in localInstructions"
             :key="index"
             class="flex gap-2 mb-2 items-start">
            <div class="text-sm font-bold mt-1">{{ index + 1 }}.</div>
            <textarea v-model="localInstructions[index]"
                      placeholder="Describe this step..."
                      class="w-full p-2 border rounded-md"
                      rows="2"></textarea>
            <Trash2 class="text-red-800 cursor-pointer mt-1"
                    @click="removeStep(index)" />
        </div>

        <button @click="addStep"
                class="bg-secondary text-text mt-4">
            <Plus class="inline-icon" /> Add Instruction
        </button>
    </div>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from 'vue';
import { Plus, Trash2 } from 'lucide-vue-next';

const props = defineProps<{
    initialInstructions: string[];
}>();

// Emits event to parent to update ingredients
const emit = defineEmits<{
    (event: 'update',
        payload: { instructions: Array<string> }): void;
}>();

const localInstructions = ref<string[]>([...props.initialInstructions]);

// Emit updated list on changes
watch(localInstructions, () => {
        emit('update', { instructions: [...localInstructions.value] });
}, { deep: true });

// Methods to manage instructions
const addStep = () => {
    localInstructions.value.push('');
};

const removeStep = (index: number) => {
    localInstructions.value.splice(index, 1);
};
</script>

<style scoped>
textarea {
    resize: none;
}
</style>