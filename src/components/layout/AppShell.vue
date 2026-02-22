<template>
  <main class="shell">
    <button v-if="showGuideButton" type="button" class="global-guide" @click="startTour">Demo Guide</button>
    <section class="content">
      <slot />
    </section>
    <AppTourOverlay
      :open="isTourOpen"
      :rect="activeRect"
      :title="activeStep.title"
      :description="activeStep.description"
      :step-index="stepIndex"
      :total="tourSteps.length"
      @close="closeTour"
      @prev="prevStep"
      @next="nextStep"
    />
  </main>
</template>

<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import AppTourOverlay from '../common/AppTourOverlay.vue';

interface TourStep {
  route: '/' | '/chat' | '/transactions';
  selector: string;
  title: string;
  description: string;
}

interface RectTarget {
  getBoundingClientRect(): { top: number; left: number; width: number; height: number };
}

interface BrowserEnv {
  document?: { querySelector(selector: string): RectTarget | null };
  addEventListener(event: string, listener: () => void, options?: boolean): void;
  removeEventListener(event: string, listener: () => void, options?: boolean): void;
}

const browser = globalThis as unknown as BrowserEnv;
const router = useRouter();
const route = useRoute();
const isTourOpen = ref(false);
const stepIndex = ref(0);
const activeRect = ref<{ top: number; left: number; width: number; height: number } | null>(null);

const tourSteps: TourStep[] = [
  {
    route: '/',
    selector: '[data-tour=\"dashboard-user-menu\"]',
    title: 'Pick Your Demo Identity',
    description: 'Use this profile menu to choose who is chatting with Sichi or switch demo users anytime.'
  },
  {
    route: '/',
    selector: '[data-tour=\"dashboard-input\"]',
    title: 'Start With A Real Issue',
    description: 'Type a banking transaction issue here. Sichi works best with real complaint-style messages.'
  },
  {
    route: '/chat',
    selector: '[data-tour=\"chat-transactions-nav\"]',
    title: 'Jump Between Chat And Records',
    description: 'From chat, open Transactions to inspect records while the conversation is ongoing.'
  },
  {
    route: '/chat',
    selector: '[data-tour=\"chat-composer\"]',
    title: 'Live Chat Experience',
    description: 'Send follow-up details here. The UI shows instant send + typing feedback while the backend responds.'
  },
  {
    route: '/transactions',
    selector: '[data-tour=\"transactions-new\"]',
    title: 'Simulate New Transactions',
    description: 'Create a transaction record to test Sichi against fresh banking events in your demo.'
  },
  {
    route: '/transactions',
    selector: '[data-tour=\"transactions-table\"]',
    title: 'Shared Transaction View',
    description: 'Review all system transactions here, copy IDs, and inspect statuses like a real support workflow.'
  }
];

const activeStep = computed(() => tourSteps[stepIndex.value] ?? tourSteps[0]);
const showGuideButton = computed(() => route.path !== '/chat');

const updateSpotlight = async (): Promise<void> => {
  if (!isTourOpen.value) return;
  await nextTick();
  const target = browser.document?.querySelector(activeStep.value.selector) ?? null;
  if (!target) {
    activeRect.value = null;
    return;
  }
  const rect = target.getBoundingClientRect();
  activeRect.value = { top: rect.top, left: rect.left, width: rect.width, height: rect.height };
};

const syncRouteForStep = async (): Promise<void> => {
  if (route.path !== activeStep.value.route) {
    await router.push(activeStep.value.route);
  }
  setTimeout(() => {
    void updateSpotlight();
  }, 120);
};

const startTour = (): void => {
  stepIndex.value = 0;
  isTourOpen.value = true;
  void syncRouteForStep();
};

const closeTour = (): void => {
  isTourOpen.value = false;
  activeRect.value = null;
};

const nextStep = (): void => {
  if (stepIndex.value >= tourSteps.length - 1) {
    closeTour();
    void router.push('/');
    return;
  }
  stepIndex.value += 1;
};

const prevStep = (): void => {
  if (stepIndex.value <= 0) return;
  stepIndex.value -= 1;
};

const handleViewportChange = (): void => {
  if (!isTourOpen.value) return;
  void updateSpotlight();
};

watch([isTourOpen, stepIndex, () => route.path], async () => {
  if (!isTourOpen.value) return;
  await syncRouteForStep();
});

browser.addEventListener('resize', handleViewportChange);
browser.addEventListener('scroll', handleViewportChange, true);

onBeforeUnmount(() => {
  browser.removeEventListener('resize', handleViewportChange);
  browser.removeEventListener('scroll', handleViewportChange, true);
});
</script>

<style scoped src="./AppShell.css"></style>
