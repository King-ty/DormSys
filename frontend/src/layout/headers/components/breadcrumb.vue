<template>
  <!-- :separator-icon="ArrowRight" -->
  <el-breadcrumb separator="/">
    <el-breadcrumb-item
      :to="item.path"
      v-for="(item, index) in routeList"
      :key="index"
    >
      <span class="no-redirect" v-if="index === routeList.length - 1">
        {{ $t(`menus.${item.name}`) }}</span
      >
      <span class="redirect" v-else>{{ $t(`menus.${item.name}`) }}</span>
    </el-breadcrumb-item>
  </el-breadcrumb>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { watch, ref } from 'vue'
// import { ArrowRight } from '@element-plus/icons-vue'

const route = useRoute()
// const router = useRouter()

const routeList = ref([])

const initRouteList = () => {
  routeList.value = route.matched
  // console.log(route.matched)
}

watch(
  route,
  () => {
    initRouteList()
  },
  { deep: true, immediate: true }
)
</script>

<style lang="scss" scoped>
.redirect {
  color: #666;
  font-weight: 600;
  &:hover {
    color: $menuBg;
  }
}
</style>
