<template>
  <section class="start-screen">
    <div class="ambient" aria-hidden="true">
      <span class="orb orb-one"></span>
      <span class="orb orb-two"></span>
      <span class="orb orb-three"></span>
    </div>
    <h1>How can I help?</h1>
    <label class="input-wrap">
      <span class="sr-only">Conversation starter</span>
      <input
        v-model="draft"
        type="text"
        :placeholder="animatedPlaceholder"
      />
    </label>
  </section>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue';

const draft = ref('');
const placeholderHints = [
  'My transfer is pending for more than 24 hours.',
  'I want to dispute a card charge.',
  'Where is my bank-to-bank transfer?',
  'I need a human support specialist.'
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
</script>

<style scoped src="./DashboardView.css"></style>
