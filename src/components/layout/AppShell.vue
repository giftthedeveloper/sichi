<template>
  <main class="shell">
    <aside class="sidebar" aria-label="Collapsed navigation">
      <div class="mark" aria-hidden="true"></div>
    </aside>
    <section class="content">
      <slot />
    </section>
  </main>
</template>

<script setup lang="ts"></script>

<style scoped src="./AppShell.css"></style>
