<template>
  <article class="panel-card">
    <header v-if="title" class="panel-head">
      <h3>{{ title }}</h3>
      <slot name="header-extra" />
    </header>
    <slot />
  </article>
</template>

<script setup lang="ts">
defineProps<{ title?: string }>();
</script>

<style scoped src="./PanelCard.css"></style>
