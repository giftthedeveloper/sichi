import { computed, onBeforeUnmount, ref, watch } from 'vue';

import type { DemoProfile } from '../types/chatSession';

const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000';

const searchProfilesRequest = async (query: string): Promise<DemoProfile[]> => {
  const response = await fetch(`${API_BASE_URL}/api/profiles?query=${encodeURIComponent(query)}`);
  if (!response.ok) throw new Error('Unable to fetch profiles');
  const data: unknown = await response.json();
  if (!Array.isArray(data)) return [];
  return data
    .filter(
      (entry): entry is DemoProfile =>
        typeof entry === 'object' &&
        entry !== null &&
        'id' in entry &&
        typeof entry.id === 'string' &&
        'name' in entry &&
        typeof entry.name === 'string'
    )
    .map((entry) => ({ id: entry.id, name: entry.name }));
};

const createProfileRequest = async (name: string): Promise<DemoProfile> => {
  const response = await fetch(`${API_BASE_URL}/api/profiles`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name })
  });
  if (!response.ok) throw new Error('Unable to create profile');
  const data: unknown = await response.json();
  if (
    typeof data === 'object' &&
    data !== null &&
    'id' in data &&
    typeof data.id === 'string' &&
    'name' in data &&
    typeof data.name === 'string'
  ) {
    return { id: data.id, name: data.name };
  }
  throw new Error('Invalid profile response');
};

export function useProfilesApi(onSelectProfile: (profile: DemoProfile) => void) {
  const profileQuery = ref('');
  const profiles = ref<DemoProfile[]>([]);
  const isSearching = ref(false);
  let debounceTimer: ReturnType<typeof setTimeout> | null = null;
  let requestToken = 0;

  const runSearch = async (query: string): Promise<void> => {
    const token = ++requestToken;
    isSearching.value = true;
    try {
      const result = await searchProfilesRequest(query);
      if (token !== requestToken) return;
      profiles.value = result;
    } catch {
      if (token === requestToken) profiles.value = [];
    } finally {
      if (token === requestToken) isSearching.value = false;
    }
  };

  watch(profileQuery, (value) => {
    const term = value.trim();
    if (debounceTimer) clearTimeout(debounceTimer);
    if (!term) {
      profiles.value = [];
      isSearching.value = false;
      return;
    }
    debounceTimer = setTimeout(() => {
      void runSearch(term);
    }, 180);
  });

  onBeforeUnmount(() => {
    if (debounceTimer) clearTimeout(debounceTimer);
  });

  const canAddQueryUser = computed(() => {
    const term = profileQuery.value.trim().toLowerCase();
    if (!term) return false;
    return !profiles.value.some((user) => user.name.trim().toLowerCase() === term);
  });

  const selectUserById = (userId: string): void => {
    const user = profiles.value.find((entry) => entry.id === userId);
    if (!user) return;
    onSelectProfile(user);
    profileQuery.value = '';
    profiles.value = [];
  };

  const addFromQuery = async (): Promise<void> => {
    const name = profileQuery.value.trim();
    if (!name) return;
    try {
      const created = await createProfileRequest(name);
      onSelectProfile(created);
      profileQuery.value = '';
      profiles.value = [];
    } catch {
      // Keep picker open so user can retry.
    }
  };

  return {
    profileQuery,
    profiles,
    isSearching,
    canAddQueryUser,
    selectUserById,
    addFromQuery
  };
}
