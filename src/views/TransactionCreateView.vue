<template>
  <section class="create-view">
    <button type="button" class="ghost" @click="router.push('/transactions')">←</button>
    <h2>Screen 4: Structured Capture</h2>
    <p>This is next. For now, new transactions must start from the transactions list screen.</p>
  </section>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();
</script>

<style scoped src="./TransactionCreateView.css"></style>
