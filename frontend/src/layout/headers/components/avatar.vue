<template>
  <el-dropdown>
    <span class="el-dropdown-link">
      <el-avatar :size="40" :src="circleUrl" />
    </span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item @click="logout">{{
          $t('login.logout')
        }}</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'

const store = useStore()

const logout = () => {
  store.dispatch('app/logout')
}

const circleUrl = ref(
  'https://ts1.cn.mm.bing.net/th/id/R-C.86a0fa17b9b37ff7518b552e2517a0ae?rik=CX0%2fMchuLIBQVA&riu=http%3a%2f%2fimg.crcz.com%2fallimg%2f201809%2f11%2f1536666825645562.jpg&ehk=g6IGr0cDabvrRd5KSQdbup2trGpltKDfA7Hx7eopcm0%3d&risl=&pid=ImgRaw&r=0&sres=1&sresct=1'
)
</script>

<style lang="scss" scoped></style>
