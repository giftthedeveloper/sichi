<template>
  <section class="transactions-view">
    <header class="top">
      <div>
        <h2>Transactions</h2>
        <p>Review all transactions in the system before creating a new one.</p>
      </div>
      <button type="button" class="new-btn" @click="router.push('/transactions/new')">
        + New Transaction
      </button>
    </header>
    <TransactionTable :rows="rows" />
  </section>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

import TransactionTable from '../components/transactions/TransactionTable.vue';
import { useTransactionsMaster } from '../composables/useTransactionsMaster';

const router = useRouter();
const { rows } = useTransactionsMaster();
</script>

<style scoped src="./TransactionsView.css"></style>
