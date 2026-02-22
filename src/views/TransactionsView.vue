<template>
  <section class="transactions-view">
    <div class="ambient" aria-hidden="true">
      <span class="orb orb-one"></span>
      <span class="orb orb-two"></span>
      <span class="orb orb-three"></span>
    </div>
    <header class="top">
      <button type="button" class="ghost nav-back" aria-label="Back to chat" @click="router.push('/chat')">←</button>
      <div class="title-block">
        <h2>Transactions</h2>
        <p>Review all transactions in the system before creating a new one.</p>
      </div>
      <div class="actions">
        <button type="button" class="new-btn" data-tour="transactions-new" @click="openCreateTransaction">
          + New Transaction
        </button>
      </div>
    </header>
    <div data-tour="transactions-table">
      <TransactionTable :rows="transactions.state.rows" />
    </div>
    <footer class="pager">
      <button type="button" class="pager-btn" :disabled="page === 1 || isLoading" @click="goPrev">Prev</button>
      <p>Page {{ page }} of {{ transactions.state.totalPages }}</p>
      <button
        type="button"
        class="pager-btn"
        :disabled="page === transactions.state.totalPages || isLoading"
        @click="goNext"
      >
        Next
      </button>
    </footer>
    <div v-if="isCreateOpen" class="overlay" @click.self="isCreateOpen = false">
      <section class="create-modal">
        <header class="modal-head">
          <h3>Create Transaction</h3>
          <button type="button" class="ghost" @click="isCreateOpen = false">X</button>
        </header>
        <form class="modal-form" @submit.prevent="submitNewTransaction">
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
          <button type="submit" class="new-btn" :disabled="!activeProfileName || isLoading">Create</button>
        </form>
      </section>
    </div>
    <ProfilePickerModal
      :open="isProfilePickerOpen"
      @close="isProfilePickerOpen = false"
      @selected="onProfileSelected"
    />
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue';
import { useRouter } from 'vue-router';

import ProfilePickerModal from '../components/common/ProfilePickerModal.vue';
import TransactionTable from '../components/transactions/TransactionTable.vue';
import { useChatSession } from '../composables/useChatSession';
import type { DemoProfile } from '../types/chatSession';
import { useTransactionsMaster } from '../composables/useTransactionsMaster';
import type { MasterTransaction } from '../types/transactionsMaster';

const router = useRouter();
const isCreateOpen = ref(false);
const isProfilePickerOpen = ref(false);
const isLoading = ref(false);
const page = ref(1);
const pageSize = 5;
const { state: chatState, selectUserProfile } = useChatSession();
const transactions = useTransactionsMaster();
const activeProfileName = computed(() => chatState.activeUser?.name ?? '');
const form = reactive<{
  type: MasterTransaction['type'];
  state: MasterTransaction['state'];
  amount: string;
}>({
  type: 'bank_transfer',
  state: 'successful',
  amount: ''
});
const loadCurrentPage = async (): Promise<void> => {
  isLoading.value = true;
  try {
    await transactions.loadTransactions(page.value, pageSize);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  void loadCurrentPage();
});

watch(page, () => {
  void loadCurrentPage();
});

const submitNewTransaction = async (): Promise<void> => {
  if (!activeProfileName.value) {
    isCreateOpen.value = false;
    isProfilePickerOpen.value = true;
    return;
  }
  if (!form.amount.trim()) return;
  isLoading.value = true;
  try {
    const accountLast4 = String(Math.floor(1000 + Math.random() * 9000));
    await transactions.addTransaction({
      profileName: activeProfileName.value,
      accountLast4,
      type: form.type,
      state: form.state,
      amount: form.amount
    });
    page.value = 1;
    await transactions.loadTransactions(1, pageSize);
    form.type = 'bank_transfer';
    form.state = 'successful';
    form.amount = '';
    isCreateOpen.value = false;
  } finally {
    isLoading.value = false;
  }
};

const openCreateTransaction = (): void => {
  if (activeProfileName.value) {
    isCreateOpen.value = true;
    return;
  }
  isProfilePickerOpen.value = true;
};

const onProfileSelected = (profile: DemoProfile): void => {
  selectUserProfile(profile);
  isProfilePickerOpen.value = false;
  isCreateOpen.value = true;
};

const goPrev = (): void => {
  page.value = Math.max(1, page.value - 1);
};

const goNext = (): void => {
  page.value = Math.min(transactions.state.totalPages, page.value + 1);
};
</script>

<style scoped src="./TransactionsView.css"></style>
<style scoped src="./TransactionsViewModal.css"></style>
