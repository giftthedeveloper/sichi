import { computed, reactive } from 'vue';

import { API_BASE_URL } from '../lib/apiBase';
import type { CaseRecord, ConversationMessage, DemoProfile } from '../types/chatSession';

interface ChatApiMessage {
  id: number;
  sender: 'user' | 'bot';
  text: string;
  created_at: string;
}

interface ChatApiResponse {
  id: string;
  profile_id: string;
  status: 'active' | 'escalated';
  detail_stage: number;
  created_at: string;
  updated_at: string;
  messages: ChatApiMessage[];
}

interface ChatState {
  activeUser: DemoProfile | null;
  activeCase: CaseRecord | null;
  messages: ConversationMessage[];
}

const state = reactive<ChatState>({
  activeUser: null,
  activeCase: null,
  messages: []
});

const toUiTime = (iso: string): string =>
  new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

const toUiMessage = (message: ChatApiMessage): ConversationMessage => ({
  id: String(message.id),
  sender: message.sender,
  text: message.text,
  time: toUiTime(message.created_at),
  createdAt: message.created_at
});

const hydrateFromApi = (payload: ChatApiResponse): void => {
  state.activeCase = {
    id: payload.id,
    status: payload.status,
    detailStage: Math.max(0, Math.min(3, payload.detail_stage)) as 0 | 1 | 2 | 3,
    createdAt: payload.created_at,
    updatedAt: payload.updated_at
  };
  state.messages = payload.messages.map(toUiMessage);
};

const removeTypingPlaceholders = (): void => {
  state.messages = state.messages.filter((message) => !message.isTyping);
};

const postJson = async <T>(path: string, body: object): Promise<T> => {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  if (!response.ok) throw new Error(`Request failed: ${path}`);
  return (await response.json()) as T;
};

export function useChatSession() {
  const needsUser = computed(() => !state.activeUser);

  const selectUserProfile = (profile: DemoProfile): void => {
    state.activeUser = profile;
  };

  const ensureSessionForActiveUser = async (): Promise<void> => {
    if (!state.activeUser) return;
    const data = await postJson<ChatApiResponse>('/api/chats/session', {
      profile_id: state.activeUser.id
    });
    hydrateFromApi(data);
  };

  const startCaseFromIssue = async (issue: string): Promise<void> => {
    if (!state.activeUser || !issue.trim()) return;
    await ensureSessionForActiveUser();
    await sendMessage(issue.trim());
  };

  const sendMessage = async (text: string): Promise<void> => {
    if (!state.activeCase || !text.trim()) return;
    const cleanText = text.trim();
    const nowIso = new Date().toISOString();
    state.messages.push({
      id: `local-user-${Date.now()}`,
      sender: 'user',
      text: cleanText,
      time: toUiTime(nowIso),
      createdAt: nowIso
    });
    state.messages.push({
      id: `local-bot-typing-${Date.now() + 1}`,
      sender: 'bot',
      text: '',
      time: '',
      createdAt: nowIso,
      isTyping: true
    });
    try {
      const data = await postJson<ChatApiResponse>(`/api/chats/${state.activeCase.id}/messages`, {
        text: cleanText
      });
      hydrateFromApi(data);
    } catch (error) {
      removeTypingPlaceholders();
      throw error;
    }
  };

  return {
    state,
    needsUser,
    selectUserProfile,
    ensureSessionForActiveUser,
    startCaseFromIssue,
    sendMessage
  };
}
