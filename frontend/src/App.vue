<template>
  <el-config-provider :locale="locale">
    <router-view />
  </el-config-provider>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
// Element语言
import zhCn from 'element-plus/lib/locale/lang/zh-cn'
import en from 'element-plus/lib/locale/lang/en'
const store = useStore()
const language = computed(() => store.getters.lang)
const lang = {
  zh: zhCn,
  en: en
}
const locale = computed(() => lang[language.value])
</script>

<style lang="scss">
.el-message-box__status {
  position: absolute !important;
}
</style>
