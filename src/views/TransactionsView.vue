<template>
  <section class="transactions-view">
    <header class="top">
      <div>
        <h2>Transactions</h2>
        <p>Review all transactions in the system before creating a new one.</p>
      </div>
      <button type="button" class="new-btn" @click="isCreateOpen = true">
        + New Transaction
      </button>
    </header>
    <TransactionTable :rows="rows" />
    <div v-if="isCreateOpen" class="overlay" @click.self="isCreateOpen = false">
      <section class="create-modal">
        <header class="modal-head">
          <h3>Create Transaction</h3>
          <button type="button" class="ghost" @click="isCreateOpen = false">X</button>
        </header>
        <form class="modal-form" @submit.prevent="submitNewTransaction">
          <label>
            Profile Name
            <input v-model="form.profileName" type="text" placeholder="e.g. Chiamaka Obi" />
          </label>
          <label>
            Type
            <select v-model="form.type">
              <option value="bank_transfer">Bank transfer</option>
              <option value="card_payment">Card payment</option>
              <option value="reversal">Reversal</option>
              <option value="pos_charge">POS charge</option>
              <option value="bills">Bills</option>
            </select>
          </label>
          <label>
            Status
            <select v-model="form.state">
              <option value="processing">Processing</option>
              <option value="review">Review</option>
              <option value="resolved">Resolved</option>
              <option value="escalated">Escalated</option>
            </select>
          </label>
          <label>
            Amount
            <input v-model="form.amount" type="text" placeholder="N25,000" />
          </label>
          <button type="submit" class="new-btn">Create</button>
        </form>
      </section>
    </div>
  </section>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';

import TransactionTable from '../components/transactions/TransactionTable.vue';
import { useTransactionsMaster } from '../composables/useTransactionsMaster';
import type { MasterTransaction } from '../types/transactionsMaster';

const isCreateOpen = ref(false);
const { rows, addTransaction } = useTransactionsMaster();
const form = reactive<{
  profileName: string;
  type: MasterTransaction['type'];
  state: MasterTransaction['state'];
  amount: string;
}>({
  profileName: '',
  type: 'bank_transfer',
  state: 'processing',
  amount: ''
});

const submitNewTransaction = (): void => {
  if (!form.profileName.trim() || !form.amount.trim()) return;
  addTransaction({
    profileName: form.profileName,
    type: form.type,
    state: form.state,
    amount: form.amount
  });
  form.profileName = '';
  form.type = 'bank_transfer';
  form.state = 'processing';
  form.amount = '';
  isCreateOpen.value = false;
};
</script>

<style scoped src="./TransactionsView.css"></style>
