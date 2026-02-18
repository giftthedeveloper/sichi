import { computed, reactive } from 'vue';

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
  status: 'active' | 'ready_to_resolve' | 'resolved' | 'escalated';
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

const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000';

const state = reactive<ChatState>({
  activeUser: null,
  activeCase: null,
  messages: []
});

const toUiTime = (iso: string): string =>
  new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

const hydrateFromApi = (payload: ChatApiResponse): void => {
  state.activeCase = {
    id: payload.id,
    status: payload.status,
    detailStage: Math.max(0, Math.min(3, payload.detail_stage)) as 0 | 1 | 2 | 3,
    createdAt: payload.created_at,
    updatedAt: payload.updated_at
  };
  state.messages = payload.messages.map((message) => ({
    id: String(message.id),
    sender: message.sender,
    text: message.text,
    time: toUiTime(message.created_at)
  }));
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
    const data = await postJson<ChatApiResponse>(`/api/chats/${state.activeCase.id}/messages`, {
      text: text.trim()
    });
    hydrateFromApi(data);
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
