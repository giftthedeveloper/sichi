<template>
  <PanelCard>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Transaction</th>
            <th>Customer</th>
            <th>Category</th>
            <th>Status</th>
            <th>Source</th>
            <th>Updated</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in rows" :key="row.id">
            <td class="mono">{{ row.id }}</td>
            <td>{{ row.customerId }}</td>
            <td>{{ row.category }}</td>
            <td><StatusChip :status="row.status" /></td>
            <td>{{ row.source }}</td>
            <td class="mono">{{ row.updatedAt }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </PanelCard>
</template>

<script setup lang="ts">
import PanelCard from '../common/PanelCard.vue';
import StatusChip from '../common/StatusChip.vue';
import type { Transaction } from '../../types/domain';

defineProps<{ rows: Transaction[] }>();
</script>

<style scoped src="./TransactionTable.css"></style>
