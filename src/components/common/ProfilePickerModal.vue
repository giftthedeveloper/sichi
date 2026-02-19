<template>
  <div v-if="open" class="overlay" @click.self="$emit('close')">
    <section class="picker-modal">
      <div class="picker-head">
        <h3>Select demo user</h3>
        <button type="button" class="close-btn" @click="$emit('close')">X</button>
      </div>
      <label class="search-box">
        <span class="sr-only">Search profile</span>
        <input v-model="profileQuery" type="text" placeholder="Search your name" />
      </label>
      <button v-if="canAddQueryUser" type="button" class="add-query-btn" @click="addUserFromQuery">
        + Add "{{ profileQuery.trim() }}"
      </button>
      <ul class="user-list">
        <li v-if="!profileQuery.trim()" class="empty-state">Start typing your name to find profile.</li>
        <li v-if="profileQuery.trim() && isSearching" class="empty-state">Searching profiles...</li>
        <li v-for="user in profiles" :key="user.id">
          <button type="button" class="user-card" @click="selectUser(user.id)">
            <span class="avatar">{{ avatarLabel(user.name) }}</span>
            <span class="identity"><strong>{{ user.name }}</strong></span>
            <span class="use-tag">+ Use</span>
          </button>
        </li>
        <li v-if="profileQuery.trim() && !isSearching && profiles.length === 0" class="empty-state">
          No profile found. Use the add button above.
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useProfilesApi } from '../../composables/useProfilesApi';
import type { DemoProfile } from '../../types/chatSession';

defineProps<{ open: boolean }>();
const emit = defineEmits<{ (event: 'close'): void; (event: 'selected', profile: DemoProfile): void }>();

const { profileQuery, profiles, isSearching, canAddQueryUser, selectUserById, addFromQuery } =
  useProfilesApi((profile) => {
    emit('selected', profile);
    emit('close');
  });

const selectUser = (userId: string): void => {
  selectUserById(userId);
};

const avatarLabel = (name: string): string => {
  return name
    .split(' ')
    .slice(0, 2)
    .map((part) => part.charAt(0))
    .join('')
    .toUpperCase();
};

const addUserFromQuery = async (): Promise<void> => {
  await addFromQuery();
};
</script>

<style scoped src="./ProfilePickerModal.css"></style>
