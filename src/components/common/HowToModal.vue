<template>
  <div v-if="open" class="overlay" @click.self="$emit('close')">
    <section class="modal">
      <header class="head">
        <h3>{{ title }}</h3>
        <button type="button" class="close" @click="$emit('close')">X</button>
      </header>
      <ol>
        <li v-for="step in steps" :key="step">{{ step }}</li>
      </ol>
    </section>
  </div>
</template>

<script setup lang="ts">
defineProps<{ open: boolean; title: string; steps: readonly string[] }>();
defineEmits<{ (event: 'close'): void }>();
</script>

<style scoped src="./HowToModal.css"></style>
