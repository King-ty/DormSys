<template>
  <el-dropdown @command="handleCommand">
    <svg-icon icon="language" />
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item command="zh" :disabled="curLang === 'zh'"
          >简体中文</el-dropdown-item
        >
        <el-dropdown-item command="en" :disabled="curLang === 'en'"
          >English</el-dropdown-item
        >
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { computed } from 'vue'
import { useStore } from 'vuex'

const i18n = useI18n()

const store = useStore()

const curLang = computed(() => {
  return i18n.locale.value
})

const handleCommand = (val) => {
  i18n.locale.value = val // 别漏了
  localStorage.setItem('lang', val)
  store.commit('app/changeLang', val)
}
</script>

<style lang="scss" scoped></style>
