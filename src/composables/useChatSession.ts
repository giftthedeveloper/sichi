import { computed, reactive } from 'vue';

import type { CaseRecord, ConversationMessage, DemoProfile } from '../types/chatSession';

interface ChatState {
  activeUser: DemoProfile | null;
  activeCase: CaseRecord | null;
  messages: ConversationMessage[];
  detailStage: 0 | 1 | 2 | 3;
}

const state = reactive<ChatState>({
  activeUser: null,
  activeCase: null,
  messages: [],
  detailStage: 0
});

const timestamp = (): string =>
  new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

const appendMessage = (sender: 'user' | 'bot', text: string): void => {
  state.messages.push({ id: crypto.randomUUID(), sender, text, time: timestamp() });
};

const humanKeywords = ['human', 'agent', 'person', 'staff'] as const;

export function useChatSession() {
  const needsUser = computed(() => !state.activeUser);

  const selectUserProfile = (profile: DemoProfile): void => {
    state.activeUser = profile;
  };

  const startCaseFromIssue = (issue: string): void => {
    if (!state.activeUser) return;
    const caseId = `SC-${Math.floor(Math.random() * 9000) + 1000}`;
    state.activeCase = {
      id: caseId,
      issue,
      status: 'gathering_info',
      createdAt: timestamp()
    };
    state.messages = [];
    state.detailStage = 0;
    appendMessage('user', issue);
    appendMessage('bot', 'I understand. Please share the transfer amount first.');
  };

  const escalateToHuman = (): void => {
    if (!state.activeCase) return;
    state.activeCase.status = 'escalated';
    appendMessage('bot', 'Done. I have moved this case to human support queue.');
  };

  const sendMessage = (text: string): void => {
    if (!state.activeCase || !text.trim()) return;
    appendMessage('user', text);
    if (humanKeywords.some((word) => text.toLowerCase().includes(word))) {
      escalateToHuman();
      return;
    }
    if (state.activeCase.status === 'escalated' || state.activeCase.status === 'resolved') {
      appendMessage('bot', 'Your case is already completed. Start a new issue for another request.');
      return;
    }
    if (state.detailStage === 0) {
      state.detailStage = 1;
      appendMessage('bot', 'Thanks. Please share transaction date and time.');
      return;
    }
    if (state.detailStage === 1) {
      state.detailStage = 2;
      appendMessage('bot', 'Got it. Please provide transaction reference or recipient account.');
      return;
    }
    if (state.detailStage === 2) {
      state.detailStage = 3;
      state.activeCase.status = 'ready_to_resolve';
      appendMessage(
        'bot',
        `Case ${state.activeCase.id} is complete. I can attempt instant check now or escalate to human support.`
      );
      return;
    }
    appendMessage('bot', 'Reply with "human" if you want escalation, or continue for more help.');
  };

  return {
    state,
    needsUser,
    selectUserProfile,
    startCaseFromIssue,
    sendMessage,
    escalateToHuman
  };
}
