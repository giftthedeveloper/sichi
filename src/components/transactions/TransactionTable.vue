<template>
  <PanelCard>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Transaction</th>
            <th>User</th>
            <th>Type</th>
            <th>Amount</th>
            <th>Status</th>
            <th>Created</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in rows" :key="row.id">
            <td class="mono">{{ row.id }}</td>
            <td>{{ row.profileName }}</td>
            <td>{{ row.type.replace('_', ' ') }}</td>
            <td class="mono">{{ row.amount }}</td>
            <td><span class="state" :class="`state-${row.state}`">{{ row.state }}</span></td>
            <td class="mono">{{ row.createdAt }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </PanelCard>
</template>

<script setup lang="ts">
import PanelCard from '../common/PanelCard.vue';
import type { MasterTransaction } from '../../types/transactionsMaster';

defineProps<{ rows: MasterTransaction[] }>();
</script>

<style scoped src="./TransactionTable.css"></style>
