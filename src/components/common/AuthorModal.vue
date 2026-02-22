<template>
  <div v-if="open" class="overlay" @click.self="$emit('close')">
    <section class="modal">
      <div class="grabber" aria-hidden="true"></div>
      <header class="head">
        <p class="eyebrow">About The Developer</p>
        <button type="button" class="close" @click="$emit('close')">X</button>
      </header>

      <section class="hero">
        <h3>Hello, my name is Gift Jeremiah.</h3>
        <p class="headline">
          I’m a software engineer, and my strongest area is backend engineering. I enjoy building reliable systems and
          clean APIs, but I also like taking ownership of features end-to-end so the final product feels complete.
        </p>
      </section>

      <section class="body">
        <p>
          I work with Python, JavaScript/TypeScript, Java, and Go. I like exploring ideas deeply, testing out what I
          know, and learning fast by building real things. I care a lot about quality, maintainability, and
          performance.
        </p>
        <p>
          Sichi is a portfolio project I built to simulate a modern banking customer support experience. It runs on a
          locally tuned Mistral model, with backend orchestration for intent routing, response boundaries, and
          tool-based checks against transaction data.
        </p>
        <p>
          I’m currently open to new opportunities, especially where I can contribute strongly on backend systems, take
          ownership, and keep growing with a sharp engineering team.
        </p>
      </section>

      <section class="links" aria-label="Contact links">
        <a class="link-card" href="mailto:giftjeremiah001@gmail.com" aria-label="Email Gift Jeremiah">
          <span class="icon" aria-hidden="true">
            <svg viewBox="0 0 24 24"><path d="M4 6h16v12H4z" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M4 7l8 6 8-6" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>
          </span>
        </a>
        <a
          class="link-card"
          href="https://github.com/giftthedeveloper"
          target="_blank"
          rel="noreferrer"
          aria-label="GitHub profile"
        >
          <span class="icon" aria-hidden="true">
            <svg viewBox="0 0 24 24"><path d="M12 3a9 9 0 0 0-2.85 17.54c.45.08.61-.19.61-.43v-1.5c-2.48.54-3-1.05-3-1.05-.4-1-.98-1.28-.98-1.28-.8-.55.06-.54.06-.54.89.06 1.35.91 1.35.91.79 1.35 2.07.96 2.58.73.08-.57.31-.96.56-1.18-1.98-.22-4.06-.99-4.06-4.4 0-.97.35-1.76.91-2.39-.09-.22-.39-1.13.09-2.36 0 0 .75-.24 2.46.91a8.43 8.43 0 0 1 4.48 0c1.71-1.15 2.46-.91 2.46-.91.48 1.23.18 2.14.09 2.36.57.63.91 1.42.91 2.39 0 3.42-2.09 4.17-4.08 4.39.32.27.61.8.61 1.62v2.4c0 .24.16.52.62.43A9 9 0 0 0 12 3Z" fill="currentColor"/></svg>
          </span>
        </a>
        <a
          class="link-card"
          href="https://www.linkedin.com/in/gift-jeremiah-1a413024b"
          target="_blank"
          rel="noreferrer"
          aria-label="LinkedIn profile"
        >
          <span class="icon" aria-hidden="true">
            <svg viewBox="0 0 24 24"><path d="M6.5 8.5V20M6.5 4.5a1.5 1.5 0 1 0 0 3a1.5 1.5 0 0 0 0-3M11 20V8.5h4v1.8c.56-1.03 1.48-2.02 3.34-2.02c3.29 0 3.66 2.53 3.66 5.8V20M15 12.1V20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </span>
        </a>
      </section>
    </section>
  </div>
</template>

<script setup lang="ts">
defineProps<{ open: boolean }>();
defineEmits<{ (event: 'close'): void }>();
</script>

<style scoped src="./AuthorModal.css"></style>
