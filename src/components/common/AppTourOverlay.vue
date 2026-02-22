<template>
  <div v-if="open" class="tour-root" @click.self="$emit('close')">
    <div class="veil"></div>
    <div v-if="rect" class="spotlight" :style="spotlightStyle">
      <div class="pulse"></div>
    </div>
    <section class="card" :style="cardStyle">
      <p class="step">Demo Tour · {{ stepIndex + 1 }} / {{ total }}</p>
      <h3>{{ title }}</h3>
      <p class="body">{{ description }}</p>
      <p v-if="!rect" class="missing">This item is not visible on this screen yet. Continue to the next step.</p>
      <div class="actions">
        <button type="button" class="ghost" @click="$emit('close')">Skip</button>
        <button type="button" class="ghost" :disabled="stepIndex === 0" @click="$emit('prev')">Back</button>
        <button type="button" class="solid" @click="$emit('next')">
          {{ stepIndex + 1 >= total ? 'Finish' : 'Next' }}
        </button>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface RectLike {
  top: number;
  left: number;
  width: number;
  height: number;
}

const props = defineProps<{
  open: boolean;
  rect: RectLike | null;
  title: string;
  description: string;
  stepIndex: number;
  total: number;
}>();

defineEmits<{ (event: 'close'): void; (event: 'prev'): void; (event: 'next'): void }>();

const viewport = globalThis as unknown as { innerWidth: number; innerHeight: number };

const spotlightStyle = computed(() => {
  if (!props.rect) return {};
  return {
    top: `${props.rect.top - 8}px`,
    left: `${props.rect.left - 8}px`,
    width: `${props.rect.width + 16}px`,
    height: `${props.rect.height + 16}px`
  };
});

const cardStyle = computed(() => {
  if (!props.rect) return { top: '84px', left: '50%', transform: 'translateX(-50%)' };
  const viewportWidth = viewport.innerWidth;
  const viewportHeight = viewport.innerHeight;
  const spaceBelow = viewportHeight - (props.rect.top + props.rect.height);
  const top =
    spaceBelow > 210 ? props.rect.top + props.rect.height + 16 : Math.max(20, props.rect.top - 190);
  const left = Math.min(Math.max(14, props.rect.left), viewportWidth - 334);
  const alignCenter = viewportWidth < 760;
  return alignCenter
    ? { top: `${Math.min(viewportHeight - 220, top)}px`, left: '50%', transform: 'translateX(-50%)' }
    : { top: `${Math.min(viewportHeight - 220, top)}px`, left: `${left}px` };
});
</script>

<style scoped src="./AppTourOverlay.css"></style>
