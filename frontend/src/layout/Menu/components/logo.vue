<template>
  <el-image class="logo-image" :src="url" fit="contain" @click="toIndex()" />
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const emits = defineEmits(['toIndex'])

defineProps({
  url: {
    type: String,
    default: '@/assets/logo.png'
  }
})

const toIndex = () => {
  router.push('/users')
  emits('toIndex')
}
</script>

<style lang="scss" scoped>
.logo-image {
  width: 200px;
  padding: 10px;
  //   background-color: grey;
  &:hover {
    cursor: pointer;
  }
}
</style>
