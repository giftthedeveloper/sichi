<template>
  <PanelCard title="Conversation">
    <template #header-extra>
      <button class="ghost" @click="$emit('escalate')">Escalate</button>
    </template>
    <div class="chat-feed">
      <p v-if="activeCustomer" class="customer-label">{{ activeCustomer.name }} · {{ activeCustomer.handle }}</p>
      <div v-for="message in messages" :key="message.id" class="bubble" :class="message.sender">
        <span>{{ message.body }}</span>
        <small>{{ message.createdAt }}</small>
      </div>
    </div>
    <form class="composer" @submit.prevent="submit">
      <input v-model="draft" placeholder="Type a customer message..." />
      <button type="submit">Send</button>
    </form>
  </PanelCard>
</template>

<script setup lang="ts">
import { ref } from 'vue';

import PanelCard from '../common/PanelCard.vue';
import type { ChatMessage, Customer } from '../../types/domain';

const props = defineProps<{ messages: ChatMessage[]; activeCustomer?: Customer }>();
const emit = defineEmits<{ (event: 'send', body: string): void; (event: 'escalate'): void }>();
const draft = ref('');

const submit = (): void => {
  const value = draft.value.trim();
  if (!value || !props.activeCustomer) return;
  emit('send', value);
  draft.value = '';
};
</script>

<style scoped src="./ChatWindow.css"></style>
