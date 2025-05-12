<template>
    <div>
        <h2 class="text-xl font-semibold mb-4">Select Tags</h2>

        <!-- Selected Tags -->
        <div v-if="selectedTags.length"
             class="flex flex-wrap gap-2 mb-4">
            <button v-for="tag in selectedTags"
                    :key="tag.id"
                    class="button-list-style bg-primary-dark text-white">
                <X @click.stop="toggleTag(tag)"
                   class="inline-icon" /> {{ tag.name }}
            </button>
        </div>

        <!-- Tag Search -->
        <input type="text"
               v-model="tagSearchQuery"
               placeholder="Search tags"
               class="w-full mb-4 px-3 py-2 border rounded-md" />

        <!-- Add new tag -->
        <button v-if="canAddNewTag"
                @click="addNewTag"
                class="button-list-style bg-secondary text-text mb-4">
            <Plus class="inline-icon" /> {{ tagSearchQuery }}
        </button>

        <!-- Tag Options -->
        <div v-if="filteredTags.length"
             class="flex flex-wrap gap-2">
            <button v-for="tag in filteredTags"
                    :key="tag.id"
                    @click="toggleTag(tag)"
                    class="button-list-style bg-gray-200 text-text">
                <Tag class="inline-icon" /> {{ tag.name }}
            </button>
        </div>

        <p v-else
           class="text-sm text-gray-500">No tags found. Try adding one?</p>
    </div>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, defineEmits, computed, onMounted } from 'vue';
import { Plus, X, Tag } from 'lucide-vue-next';
import { getTags, createTag } from '@services/api';
import type { TagType } from '@/types';

// Props and Emits
const props = defineProps<{
    initialTags: TagType[];
}>();

const emit = defineEmits<{
    (event: 'update', payload: {tags: TagType[]}): void;
}>();

// Local state
const selectedTags = ref<TagType[]>([...props.initialTags]);
const filteredTags = ref<TagType[]>([]);
const allTags = ref<TagType[]>([]);
const tagSearchQuery = ref('');

watch(selectedTags, () => {
    emit('update', {tags: [...selectedTags.value]});
}, { deep: true });

const toggleTag = (tag: TagType) => {
    const index = selectedTags.value.findIndex(t => t.id === tag.id);
    if (index >= 0) {
        selectedTags.value.splice(index, 1);
    } else {
        selectedTags.value.push(tag);
    }
};

watch(tagSearchQuery, () => {
    const query = tagSearchQuery.value.toLowerCase();
    filteredTags.value = allTags.value.filter(tag =>
        tag.name.toLowerCase().includes(query) &&
        !selectedTags.value.some(t => t.id === tag.id)
    );
});

const canAddNewTag = computed(() => {
    const query = tagSearchQuery.value.trim().toLowerCase();
    return query.length > 1 &&
        !allTags.value.some(tag => tag.name.toLowerCase() === query);
});

const addNewTag = async () => {
    try {
        const normalizedName = tagSearchQuery.value.trim().replace(/\s+/g, ' ');
        const capitalized = normalizedName.charAt(0).toUpperCase() + normalizedName.slice(1);
        const response = await createTag(capitalized.trim());
        const newTag = response.data;
        allTags.value.push(newTag);
        selectedTags.value.push(newTag);
        tagSearchQuery.value = '';
    } catch (error) {
        console.error('Failed to create tag:', error);
    }
};

// === Initial Fetch ===
onMounted(async () => {
    try {
        const response = await getTags();
        allTags.value = response.data;
        filteredTags.value = response.data;
    } catch (error) {
        console.error('Error fetching tags:', error);
    }
});

</script>

<style scoped>
@import "@/style.css";

.inline-icon {
    @apply h-4 w-4 mr-1;
}
</style>