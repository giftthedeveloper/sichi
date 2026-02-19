<template>
  <PanelCard>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Transaction</th>
            <th>User</th>
            <th>Account Number</th>
            <th>Type</th>
            <th>Amount</th>
            <th>Status</th>
            <th>Transaction Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in rows" :key="row.id">
            <td>
              <div class="id-cell">
                <button
                  type="button"
                  class="copy-btn"
                  :aria-label="copiedId === row.id ? 'Copied transaction ID' : 'Copy transaction ID'"
                  @click="copyId(row.id)"
                >
                  <svg v-if="copiedId === row.id" viewBox="0 0 24 24" aria-hidden="true">
                    <path
                      d="M20 6L9 17l-5-5"
                      fill="none"
                      stroke="currentColor"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                    />
                  </svg>
                  <svg v-else viewBox="0 0 24 24" aria-hidden="true">
                    <rect x="9" y="9" width="11" height="11" rx="2" fill="none" stroke="currentColor" stroke-width="2" />
                    <path
                      d="M5 15V6a2 2 0 0 1 2-2h9"
                      fill="none"
                      stroke="currentColor"
                      stroke-linecap="round"
                      stroke-width="2"
                    />
                  </svg>
                </button>
                <span class="mono">{{ row.id }}</span>
              </div>
            </td>
            <td>{{ row.profileName }}</td>
            <td class="mono">******{{ row.accountLast4 }}</td>
            <td>{{ row.type.replace('_', ' ') }}</td>
            <td class="mono">{{ row.amount }}</td>
            <td><span class="state" :class="`state-${row.state}`">{{ row.state }}</span></td>
            <td class="mono">{{ row.transactionDate }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </PanelCard>
</template>

<script setup lang="ts">
import { ref } from 'vue';

import PanelCard from '../common/PanelCard.vue';
import type { MasterTransaction } from '../../types/transactionsMaster';

defineProps<{ rows: MasterTransaction[] }>();

const copiedId = ref('');

const copyId = async (id: string): Promise<void> => {
  const nav = navigator as Navigator & { clipboard?: { writeText(text: string): Promise<void> } };
  try {
    if (nav.clipboard) {
      await nav.clipboard.writeText(id);
    } else {
      throw new Error('Clipboard unavailable');
    }
    copiedId.value = id;
    setTimeout(() => {
      if (copiedId.value === id) copiedId.value = '';
    }, 1200);
  } catch {
    copiedId.value = '';
  }
};
</script>

<style scoped src="./TransactionTable.css"></style>
