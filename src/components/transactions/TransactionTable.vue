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
                <span class="mono">{{ row.id }}</span>
                <button type="button" class="copy-btn" @click="copyId(row.id)">
                  {{ copiedId === row.id ? 'Copied' : 'Copy' }}
                </button>
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
