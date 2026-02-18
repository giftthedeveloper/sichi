<template>
  <PanelCard title="Transaction Detail">
    <template v-if="transaction">
      <div class="stats">
        <div>
          <p>ID</p>
          <strong class="mono">{{ transaction.id }}</strong>
        </div>
        <div>
          <p>Amount</p>
          <strong class="mono">{{ transaction.amount }}</strong>
        </div>
        <div>
          <p>Category</p>
          <strong>{{ transaction.category }}</strong>
        </div>
      </div>
      <StatusChip :status="transaction.status" />
      <ul class="timeline">
        <li v-for="event in events" :key="event.id">
          <strong>{{ event.title }}</strong>
          <p>{{ event.note }}</p>
          <small class="mono">{{ event.time }}</small>
        </li>
      </ul>
    </template>
    <p v-else class="empty">Select a customer with a transaction case.</p>
  </PanelCard>
</template>

<script setup lang="ts">
import PanelCard from '../common/PanelCard.vue';
import StatusChip from '../common/StatusChip.vue';
import type { TimelineEvent, Transaction } from '../../types/domain';

defineProps<{ transaction?: Transaction; events: TimelineEvent[] }>();
</script>

<style scoped src="./TransactionPanel.css"></style>
