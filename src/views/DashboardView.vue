<template>
  <section class="start-screen">
    <div class="ambient" aria-hidden="true">
      <span class="orb orb-one"></span>
      <span class="orb orb-two"></span>
      <span class="orb orb-three"></span>
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
      </label>
      <button type="submit" aria-label="Send message">Send</button>
    </form>
  </section>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue';

const draft = ref('');
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
  if (!draft.value.trim()) return;
  // Screen 1 is mock-only for now, so submission clears the field.
  draft.value = '';
};
</script>

<style scoped src="./DashboardView.css"></style>
