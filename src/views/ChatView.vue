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
      <div class="spacer"></div>
    </header>

    <section v-if="!session.activeCase" class="empty">
      <h2>No active case yet</h2>
      <p>Go back and submit an issue from Screen 1.</p>
    </section>

    <section v-else class="chat-body">
      <div class="thread">
        <article v-for="message in session.messages" :key="message.id" class="bubble" :class="message.sender">
          <p>{{ message.text }}</p>
          <small>{{ message.time }}</small>
        </article>
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

const router = useRouter();
const draft = ref('');
const isSending = ref(false);
const { state: session, sendMessage, ensureSessionForActiveUser } = useChatSession();

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

const submitMessage = async (): Promise<void> => {
  const text = draft.value.trim();
  if (!text) return;
  isSending.value = true;
  try {
    await sendMessage(text);
    draft.value = '';
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
