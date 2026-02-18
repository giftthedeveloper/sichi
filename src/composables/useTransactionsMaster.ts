import { computed, reactive } from 'vue';

import { transactionsSeed } from '../data/transactionsSeed';
import type { MasterTransaction } from '../types/transactionsMaster';

interface TransactionsState {
  rows: MasterTransaction[];
}

const state = reactive<TransactionsState>({
  rows: [...transactionsSeed]
});

export function useTransactionsMaster() {
  const rows = computed(() => state.rows);

  return {
    rows
  };
}
