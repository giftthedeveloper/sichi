<template>
  <main class="shell">
    <button type="button" class="global-guide" @click="isGuideOpen = true">Demo Guide</button>
    <section class="content">
      <slot />
    </section>
    <HowToModal :open="isGuideOpen" title="Sichi Demo Guide" :steps="guideSteps" @close="isGuideOpen = false" />
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue';

import HowToModal from '../common/HowToModal.vue';

const isGuideOpen = ref(false);
const guideSteps = [
  'Select or add a demo user from the top-right profile control.',
  'Start a chat with a bank issue and follow Sichi prompts.',
  'Open Transactions to review records across users.',
  'Create a new transaction with your active demo user.',
  'Use the copy icon beside any transaction ID when needed.'
] as const;
</script>

<style scoped src="./AppShell.css"></style>
