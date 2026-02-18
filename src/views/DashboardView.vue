<template>
  <section class="start-screen">
    <div class="ambient" aria-hidden="true">
      <span class="orb orb-one"></span>
      <span class="orb orb-two"></span>
      <span class="orb orb-three"></span>
    </div>
    <div class="login-row">
      <button type="button" class="picker-btn" @click="isPickerOpen = true">
        Select demo user
      </button>
      <p v-if="selectedUser" class="user-chip">{{ selectedUser.name }}</p>
    </div>
    <h1>How can I help?</h1>
    <form class="input-wrap" @submit.prevent="submitStarter">
      <label class="field">
        <span class="sr-only">Conversation starter</span>
        <input
          v-model="draft"
          type="text"
          :placeholder="animatedPlaceholder"
        />
        <button type="submit" class="send-icon" aria-label="Send message">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path
              d="M4 20L21 12L4 4L4 10L15 12L4 14L4 20Z"
              fill="currentColor"
            />
          </svg>
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
          <input
            v-model="profileQuery"
            type="text"
            placeholder="Search your name"
          />
        </label>
        <button
          v-if="canAddQueryUser"
          type="button"
          class="add-query-btn"
          @click="addFromQuery"
        >
          + Add "{{ profileQuery.trim() }}"
        </button>
        <ul class="user-list">
          <li v-if="!profileQuery.trim()" class="empty-state">
            Start typing your name to find profile.
          </li>
          <li v-for="user in filteredUsers" :key="user.id">
            <button type="button" class="user-card" @click="selectUser(user.id)">
              <span class="avatar">{{ avatarLabel(user.name) }}</span>
              <span class="identity"><strong>{{ user.name }}</strong></span>
              <span class="use-tag">+ Use</span>
            </button>
          </li>
          <li v-if="profileQuery.trim() && filteredUsers.length === 0" class="empty-state">
            No profile found. Use the add button above.
          </li>
        </ul>
      </section>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';

interface DemoUser {
  id: string;
  name: string;
}

const draft = ref('');
const isPickerOpen = ref(true);
const selectedUser = ref<DemoUser | null>(null);
const profileQuery = ref('');
const demoUsers = ref<DemoUser[]>([
  {
    id: 'u-1',
    name: 'Amaka Eze'
  },
  {
    id: 'u-2',
    name: 'Tosin Akin'
  },
  {
    id: 'u-3',
    name: 'Sade Bello'
  }
]);
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
  runPlaceholderAnimation();
});

onBeforeUnmount(() => {
  if (timerId) clearTimeout(timerId);
});

const submitStarter = (): void => {
  if (!selectedUser.value || !draft.value.trim()) return;
  // Screen 1 is mock-only for now, so submission clears the field.
  draft.value = '';
};

const selectUser = (userId: string): void => {
  const picked = demoUsers.value.find((user) => user.id === userId);
  if (!picked) return;
  selectedUser.value = picked;
  isPickerOpen.value = false;
  profileQuery.value = '';
};

const avatarLabel = (name: string): string => {
  return name
    .split(' ')
    .slice(0, 2)
    .map((part) => part.charAt(0))
    .join('')
    .toUpperCase();
};

const normalized = (value: string): string => value.trim().toLowerCase();

const filteredUsers = computed(() => {
  const term = normalized(profileQuery.value);
  if (!term) return [];
  return demoUsers.value.filter((user) => normalized(user.name).includes(term));
});

const canAddQueryUser = computed(() => {
  const term = normalized(profileQuery.value);
  if (!term) return false;
  return !demoUsers.value.some((user) => normalized(user.name) === term);
});

const addFromQuery = (): void => {
  const name = profileQuery.value.trim();
  if (!name) return;
  const user: DemoUser = { id: `u-${demoUsers.value.length + 1}`, name };
  demoUsers.value.unshift(user);
  selectedUser.value = user;
  isPickerOpen.value = false;
  profileQuery.value = '';
};
</script>

<style scoped src="./DashboardView.css"></style>
<style scoped src="./DashboardViewPicker.css"></style>
