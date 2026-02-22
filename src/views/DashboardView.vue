<template>
  <section class="start-screen">
    <div class="ambient" aria-hidden="true">
      <span class="orb orb-one"></span>
      <span class="orb orb-two"></span>
      <span class="orb orb-three"></span>
    </div>
    <div class="login-row">
      <button type="button" class="picker-btn" @click="router.push('/transactions')">Transactions</button>
      <div class="user-menu">
        <button type="button" class="picker-btn user-menu-trigger" data-tour="dashboard-user-menu" @click="toggleUserMenu">
          {{ selectedUser ? selectedUser.name : 'Select demo user' }}
          <span class="caret" aria-hidden="true">▾</span>
        </button>
        <div v-if="isUserMenuOpen" class="user-menu-panel">
          <button type="button" class="user-menu-item" @click="openProfilePickerFromMenu">Change demo user</button>
        </div>
      </div>
    </div>
    <h1>How can I help?</h1>
    <form class="input-wrap" @submit.prevent="submitStarter">
      <label class="field">
        <span class="sr-only">Conversation starter</span>
        <input v-model="draft" data-tour="dashboard-input" type="text" :placeholder="animatedPlaceholder" />
        <button type="submit" class="send-icon" :disabled="isSubmittingIssue" aria-label="Send message">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20L21 12L4 4L4 10L15 12L4 14L4 20Z" fill="currentColor" /></svg>
        </button>
      </label>
    </form>
    <div v-if="isPickerOpen" class="overlay" @click.self="isPickerOpen = false">
      <section class="picker-modal">
        <div class="picker-head">
          <h2>Choose a demo profile</h2>
          <button type="button" class="close-btn" @click="isPickerOpen = false">X</button>
        </div>
        <label class="search-box">
          <span class="sr-only">Search profile</span>
          <input v-model="profileQuery" type="text" placeholder="Search your name" />
        </label>
        <button v-if="canAddQueryUser" type="button" class="add-query-btn" @click="addUserFromQuery">
          + Add "{{ profileQuery.trim() }}"
        </button>
        <ul class="user-list">
          <li v-if="!profileQuery.trim()" class="empty-state">
            Start typing your name to find profile.
          </li>
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
  </section>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

import { useProfilesApi } from '../composables/useProfilesApi';
import { useChatSession } from '../composables/useChatSession';

const draft = ref('');
const isPickerOpen = ref(false);
const isUserMenuOpen = ref(false);
const isSubmittingIssue = ref(false);
const router = useRouter();
const { state: chatState, selectUserProfile, startCaseFromIssue } = useChatSession();
const selectedUser = computed(() => chatState.activeUser);
const { profileQuery, profiles, isSearching, canAddQueryUser, selectUserById, addFromQuery } =
  useProfilesApi((profile) => {
    selectUserProfile(profile);
    isUserMenuOpen.value = false;
    isPickerOpen.value = false;
  });
const placeholderHints = [
  'I sent N25,000 since morning and it is still pending.',
  'I got debit alert but the receiver did not get the money.',
  'My account was debited twice for one POS payment.',
  'I did transfer to wrong account number, please help me urgently.',
  'Web payment failed but my account was debited.',
  'Please check why my reversal has not dropped since yesterday.'
] as const;
const animatedPlaceholder = ref('');

let hintIndex = 0;
let charIndex = 0;
let deleting = false;
let timerId: ReturnType<typeof setTimeout> | null = null;

const runPlaceholderAnimation = (): void => {
  const current = placeholderHints[hintIndex];
  if (!deleting) {
    charIndex += 1;
    animatedPlaceholder.value = current.slice(0, charIndex);
    if (charIndex >= current.length) {
      deleting = true;
      timerId = setTimeout(runPlaceholderAnimation, 1300);
      return;
    }
    timerId = setTimeout(runPlaceholderAnimation, 45);
    return;
  }
  charIndex -= 1;
  animatedPlaceholder.value = current.slice(0, charIndex);
  if (charIndex <= 0) {
    deleting = false;
    hintIndex = (hintIndex + 1) % placeholderHints.length;
    timerId = setTimeout(runPlaceholderAnimation, 220);
    return;
  }
  timerId = setTimeout(runPlaceholderAnimation, 20);
};

onMounted(() => {
  if (!selectedUser.value) {
    isPickerOpen.value = true;
  }
  runPlaceholderAnimation();
});

onBeforeUnmount(() => {
  if (timerId) clearTimeout(timerId);
});

const submitStarter = async (): Promise<void> => {
  if (!selectedUser.value || !draft.value.trim()) return;
  isSubmittingIssue.value = true;
  try {
    await startCaseFromIssue(draft.value.trim());
    draft.value = '';
    router.push('/chat');
  } finally {
    isSubmittingIssue.value = false;
  }
};

const toggleUserMenu = (): void => {
  if (!selectedUser.value) {
    isPickerOpen.value = true;
    isUserMenuOpen.value = false;
    return;
  }
  isUserMenuOpen.value = !isUserMenuOpen.value;
};

const openProfilePickerFromMenu = (): void => {
  isUserMenuOpen.value = false;
  isPickerOpen.value = true;
};

const selectUser = (userId: string): void => {
  selectUserById(userId);
  isUserMenuOpen.value = false;
  isPickerOpen.value = false;
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
  isUserMenuOpen.value = false;
  isPickerOpen.value = false;
};
</script>

<style scoped src="./DashboardView.css"></style>
<style scoped src="./DashboardViewPicker.css"></style>
