<template>
  <section class="transactions-view">
    <div class="ambient" aria-hidden="true">
      <span class="orb orb-one"></span>
      <span class="orb orb-two"></span>
      <span class="orb orb-three"></span>
    </div>
    <header class="top">
      <div>
        <h2>Transactions</h2>
        <p>Review all transactions in the system before creating a new one.</p>
      </div>
      <div class="actions">
        <button type="button" class="ghost-mini" @click="isHowToOpen = true">How To</button>
        <button type="button" class="new-btn" @click="isCreateOpen = true">+ New Transaction</button>
      </div>
    </header>
    <TransactionTable :rows="pagedRows" />
    <footer class="pager">
      <button type="button" class="pager-btn" :disabled="page === 1" @click="goPrev">Prev</button>
      <p>Page {{ page }} of {{ totalPages }}</p>
      <button type="button" class="pager-btn" :disabled="page === totalPages" @click="goNext">Next</button>
    </footer>
    <div v-if="isCreateOpen" class="overlay" @click.self="isCreateOpen = false">
      <section class="create-modal">
        <header class="modal-head">
          <h3>Create Transaction</h3>
          <button type="button" class="ghost" @click="isCreateOpen = false">X</button>
        </header>
        <form class="modal-form" @submit.prevent="submitNewTransaction">
          <p class="linked-user">
            Profile: <strong>{{ activeProfileName || 'No demo user selected' }}</strong>
          </p>
          <label>
            Account Number
            <input v-model="form.accountNumber" type="text" placeholder="e.g. 0123456789" />
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
              <option value="successful">Successful</option>
              <option value="failed">Failed</option>
            </select>
          </label>
          <label>
            Amount
            <input v-model="form.amount" type="text" placeholder="N25,000" />
          </label>
          <button type="submit" class="new-btn" :disabled="!activeProfileName">Create</button>
        </form>
      </section>
    </div>
    <HowToModal :open="isHowToOpen" title="How To Use Transactions" :steps="howToSteps" @close="isHowToOpen = false" />
  </section>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue';

import HowToModal from '../components/common/HowToModal.vue';
import TransactionTable from '../components/transactions/TransactionTable.vue';
import { useChatSession } from '../composables/useChatSession';
import { useTransactionsMaster } from '../composables/useTransactionsMaster';
import type { MasterTransaction } from '../types/transactionsMaster';

const isCreateOpen = ref(false);
const isHowToOpen = ref(false);
const page = ref(1);
const pageSize = 5;
const { state: chatState } = useChatSession();
const { rows, addTransaction } = useTransactionsMaster();
const activeProfileName = computed(() => chatState.activeUser?.name ?? '');
const totalPages = computed(() => Math.max(1, Math.ceil(rows.value.length / pageSize)));
const pagedRows = computed(() => {
  const start = (page.value - 1) * pageSize;
  return rows.value.slice(start, start + pageSize);
});
const form = reactive<{
  accountNumber: string;
  type: MasterTransaction['type'];
  state: MasterTransaction['state'];
  amount: string;
}>({
  accountNumber: '',
  type: 'bank_transfer',
  state: 'successful',
  amount: ''
});
const howToSteps = [
  'Review transactions list first before adding a new one.',
  'Use pagination at bottom to move through transaction pages.',
  'Click Copy beside any transaction ID when you need to reuse it.',
  'Click + New Transaction to open modal and create a new record.',
  'Account number is masked automatically to last 4 digits.'
] as const;

const submitNewTransaction = (): void => {
  const digits = form.accountNumber.replaceAll(/\D/g, '');
  if (!activeProfileName.value || !form.amount.trim() || digits.length < 4) return;
  addTransaction({
    profileName: activeProfileName.value,
    accountLast4: digits.slice(-4),
    type: form.type,
    state: form.state,
    amount: form.amount
  });
  page.value = 1;
  form.accountNumber = '';
  form.type = 'bank_transfer';
  form.state = 'successful';
  form.amount = '';
  isCreateOpen.value = false;
};

const goPrev = (): void => {
  page.value = Math.max(1, page.value - 1);
};

const goNext = (): void => {
  page.value = Math.min(totalPages.value, page.value + 1);
};
</script>

<style scoped src="./TransactionsView.css"></style>
<style scoped src="./TransactionsViewModal.css"></style>
