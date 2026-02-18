<template>
  <span class="chip" :class="toneClass">{{ label }}</span>
</template>

<script setup lang="ts">
import { computed } from 'vue';

import type { TicketStatus } from '../../types/domain';

const props = defineProps<{ status: TicketStatus; label?: string }>();

const toneClass = computed(() => `tone-${props.status}`);
const label = computed(() => props.label ?? props.status.replaceAll('_', ' '));
</script>

<style scoped src="./StatusChip.css"></style>
