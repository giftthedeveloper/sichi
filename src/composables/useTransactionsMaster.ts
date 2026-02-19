import { reactive } from 'vue';

import type { MasterTransaction } from '../types/transactionsMaster';

interface TransactionsApiItem {
  id: string;
  profile_name: string;
  account_last4: string;
  type: MasterTransaction['type'];
  amount: string;
  state: MasterTransaction['state'];
  transaction_date: string;
}

interface TransactionsApiResponse {
  items: TransactionsApiItem[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}

interface TransactionsState {
  rows: MasterTransaction[];
  totalPages: number;
  total: number;
}

const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000';

const state = reactive<TransactionsState>({
  rows: [],
  totalPages: 1,
  total: 0
});

const mapItem = (item: TransactionsApiItem): MasterTransaction => ({
  id: item.id,
  profileName: item.profile_name,
  accountLast4: item.account_last4,
  type: item.type,
  amount: item.amount,
  state: item.state,
  transactionDate: new Date(item.transaction_date).toLocaleString()
});

export function useTransactionsMaster() {
  const loadTransactions = async (page: number, pageSize: number): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/api/transactions?page=${page}&page_size=${pageSize}`);
    if (!response.ok) throw new Error('Unable to load transactions');
    const data = (await response.json()) as TransactionsApiResponse;
    state.rows = data.items.map(mapItem);
    state.totalPages = data.total_pages;
    state.total = data.total;
  };

  const addTransaction = async (input: {
    profileName: string;
    accountLast4: string;
    type: MasterTransaction['type'];
    amount: string;
    state: MasterTransaction['state'];
  }): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/api/transactions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        profile_name: input.profileName,
        account_last4: input.accountLast4,
        type: input.type,
        amount: input.amount,
        state: input.state
      })
    });
    if (!response.ok) throw new Error('Unable to create transaction');
  };

  return {
    state,
    loadTransactions,
    addTransaction
  };
}
