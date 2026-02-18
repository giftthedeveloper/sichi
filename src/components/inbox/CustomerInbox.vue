<template>
  <PanelCard title="Customers">
    <ul class="inbox-list">
      <li v-for="customer in customers" :key="customer.id">
        <button class="item" :class="{ active: customer.id === activeCustomerId }" @click="$emit('select', customer.id)">
          <div>
            <strong>{{ customer.name }}</strong>
            <p>{{ customer.handle }}</p>
          </div>
          <div class="meta">
            <StatusChip :status="customer.status" />
            <span v-if="customer.unread > 0" class="badge">{{ customer.unread }}</span>
          </div>
        </button>
      </li>
    </ul>
  </PanelCard>
</template>

<script setup lang="ts">
import PanelCard from '../common/PanelCard.vue';
import StatusChip from '../common/StatusChip.vue';
import type { Customer } from '../../types/domain';

defineProps<{ customers: Customer[]; activeCustomerId: string }>();

defineEmits<{ (event: 'select', id: string): void }>();
</script>

<style scoped src="./CustomerInbox.css"></style>
