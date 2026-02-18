<template>
  <PanelCard title="Simulation Lab">
    <form class="grid" @submit.prevent="submit">
      <label>
        Customer
        <select v-model="customerId">
          <option v-for="customer in customers" :key="customer.id" :value="customer.id">
            {{ customer.name }}
          </option>
        </select>
      </label>
      <label>
        Category
        <select v-model="category">
          <option value="transfer_status">Transfer status</option>
          <option value="failed_transfer">Failed transfer</option>
          <option value="card_dispute">Card dispute</option>
          <option value="account_security">Account security</option>
        </select>
      </label>
      <label>
        Amount
        <input v-model="amount" placeholder="$125.00" />
      </label>
      <button type="submit">Create Mock Transaction</button>
    </form>
  </PanelCard>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';

import PanelCard from '../common/PanelCard.vue';
import { useMockSupport } from '../../composables/useMockSupport';
import type { NewSimulationInput, Transaction } from '../../types/domain';

const emit = defineEmits<{ (event: 'create', payload: NewSimulationInput): void }>();
const { state } = useMockSupport();
const customers = computed(() => state.customers);
const customerId = ref(state.activeCustomerId);
const amount = ref('$125.00');
const category = ref<Transaction['category']>('transfer_status');

const submit = (): void => {
  const payload: NewSimulationInput = {
    customerId: customerId.value,
    amount: amount.value,
    category: category.value
  };
  emit('create', payload);
};
</script>

<style scoped src="./TransactionSimulator.css"></style>
