<template>
  <section class="chat-page">
    <div class="ambient" aria-hidden="true">
      <span class="orb orb-one"></span>
      <span class="orb orb-two"></span>
      <span class="orb orb-three"></span>
    </div>
    <header class="chat-top">
      <button type="button" class="ghost" aria-label="Go back" @click="router.push('/')">←</button>
      <div v-if="session.activeCase" class="case-pill">
        <strong>{{ session.activeCase.id }}</strong>
        <span>{{ statusLabel }}</span>
      </div>
      <button type="button" class="ghost wide" @click="router.push('/transactions')">Transactions</button>
    </header>

    <section v-if="!session.activeCase" class="empty">
      <h2>No active case yet</h2>
      <p>Go back and submit an issue from Screen 1.</p>
    </section>

    <section v-else class="chat-body">
      <div class="thread">
        <template v-for="item in threadItems" :key="item.id">
          <p v-if="item.kind === 'separator'" class="date-separator">{{ item.label }}</p>
          <article v-else class="bubble" :class="[item.message.sender, { typing: item.message.isTyping }]">
            <div v-if="item.message.isTyping" class="typing-dots" aria-label="Sichi is typing">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <p v-else>{{ item.message.text }}</p>
            <small v-if="!item.message.isTyping">{{ item.message.time }}</small>
          </article>
        </template>
      </div>
      <form class="composer" @submit.prevent="submitMessage">
        <label class="field">
          <span class="sr-only">Type message</span>
          <input v-model="draft" type="text" :placeholder="inputPlaceholder" />
          <button type="submit" class="send-icon" :disabled="isSending" aria-label="Send">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M4 20L21 12L4 4L4 10L15 12L4 14L4 20Z" fill="currentColor" />
            </svg>
          </button>
        </label>
      </form>
    </section>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

import { useChatSession } from '../composables/useChatSession';
import type { ConversationMessage } from '../types/chatSession';

const router = useRouter();
const draft = ref('');
const isSending = ref(false);
const { state: session, sendMessage, ensureSessionForActiveUser } = useChatSession();

type ThreadItem =
  | { id: string; kind: 'separator'; label: string }
  | { id: string; kind: 'message'; message: ConversationMessage };

const statusLabel = computed(() => {
  const status = session.activeCase?.status;
  if (!status) return '';
  return status.replaceAll('_', ' ');
});

const inputPlaceholder = computed(() => {
  const stage = session.activeCase?.detailStage ?? 0;
  if (stage === 0) return 'Enter transfer amount';
  if (stage === 1) return 'Enter date and time';
  if (stage === 2) return 'Enter transaction reference';
  return 'Type a follow-up or request human support';
});

const sameLocalDate = (left: Date, right: Date): boolean =>
  left.getFullYear() === right.getFullYear() &&
  left.getMonth() === right.getMonth() &&
  left.getDate() === right.getDate();

const dateLabel = (iso: string): string => {
  const target = new Date(iso);
  const now = new Date();
  const yesterday = new Date();
  yesterday.setDate(now.getDate() - 1);
  if (sameLocalDate(target, now)) return 'Today';
  if (sameLocalDate(target, yesterday)) return 'Yesterday';
  return target.toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' });
};

const threadItems = computed<ThreadItem[]>(() => {
  const items: ThreadItem[] = [];
  let previousLabel = '';
  for (const message of session.messages) {
    const label = dateLabel(message.createdAt);
    if (label !== previousLabel) {
      items.push({ id: `sep-${message.id}`, kind: 'separator', label });
      previousLabel = label;
    }
    items.push({ id: `msg-${message.id}`, kind: 'message', message });
  }
  return items;
});

const submitMessage = async (): Promise<void> => {
  const text = draft.value.trim();
  if (!text) return;
  draft.value = '';
  isSending.value = true;
  try {
    await sendMessage(text);
  } finally {
    isSending.value = false;
  }
};

onMounted(() => {
  if (!session.activeCase && session.activeUser) {
    void ensureSessionForActiveUser();
  }
});
</script>

<style scoped src="./ChatView.css"></style>
<style scoped src="./ChatViewAmbient.css"></style>
