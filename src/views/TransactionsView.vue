<template>
  <section class="transactions-view">
    <header>
      <h2>Master Transactions</h2>
      <p>All mock conversations and transaction support cases in one view.</p>
    </header>
    <TransactionTable :rows="state.transactions" />
  </section>
</template>

<script setup lang="ts">
import TransactionTable from '../components/transactions/TransactionTable.vue';
import { useMockSupport } from '../composables/useMockSupport';

const { state } = useMockSupport();
</script>

<style scoped src="./TransactionsView.css"></style>
