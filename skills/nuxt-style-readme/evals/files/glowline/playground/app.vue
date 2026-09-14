<script setup lang="ts">
import { vGlowline } from 'glowline'
</script>

<template>
  <main>
    <h1 v-glowline>Hover me</h1>
    <p v-glowline="{ colors: ['#ff0080', '#7928ca'], thickness: 4 }">Custom colors and thickness</p>
  </main>
</template>
