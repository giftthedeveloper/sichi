import { computed, reactive } from 'vue';

import { transactionsSeed } from '../data/transactionsSeed';
import type { MasterTransaction } from '../types/transactionsMaster';

interface TransactionsState {
  rows: MasterTransaction[];
}

const state = reactive<TransactionsState>({
  rows: [...transactionsSeed]
});

const nowStamp = (): string => {
  const date = new Date();
  const yyyy = date.getFullYear();
  const mm = String(date.getMonth() + 1).padStart(2, '0');
  const dd = String(date.getDate()).padStart(2, '0');
  const hh = String(date.getHours()).padStart(2, '0');
  const min = String(date.getMinutes()).padStart(2, '0');
  return `${yyyy}-${mm}-${dd} ${hh}:${min}`;
};

export function useTransactionsMaster() {
  const rows = computed(() => state.rows);

  const addTransaction = (input: {
    profileName: string;
    accountLast4: string;
    type: MasterTransaction['type'];
    amount: string;
    state: MasterTransaction['state'];
  }): void => {
    const nextId = `TXN-${Math.floor(Math.random() * 90000) + 10000}`;
    state.rows.unshift({
      id: nextId,
      profileName: input.profileName.trim(),
      accountLast4: input.accountLast4.trim(),
      type: input.type,
      amount: input.amount.trim(),
      state: input.state,
      transactionDate: nowStamp()
    });
  };

  return {
    rows,
    addTransaction
  };
}
