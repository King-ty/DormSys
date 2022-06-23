<template>
  <!-- :active-text-color="variables.menuActiveText"
    :background-color="variables.menuBg" -->
  <el-menu
    active-text-color="#ffd04b"
    background-color="#545c64"
    class="el-menu-vertical-demo"
    :default-active="defaultActive"
    text-color="#fff"
    router
    unique-opened
    :collapse="!$store.getters.siderType"
  >
    <el-sub-menu
      :index="item.id + ''"
      v-for="(item, index) in menusList"
      :key="item.id"
    >
      <template #title>
        <el-icon>
          <component :is="iconList[index]"></component>
        </el-icon>
        <span>{{ $t(`menus.${item.path}`) }}</span>
      </template>
      <el-menu-item
        :index="'/' + it.path"
        v-for="it in item.children"
        :key="it.id"
        @click="savePath(it.path)"
      >
        <template #title>
          <el-icon>
            <component :is="icon"></component>
          </el-icon>
          <span>{{ $t(`menus.${it.path}`) }}</span>
        </template>
      </el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<script setup>
import { menuList } from '@/api/menu'
import { ref } from 'vue'

const iconList = ref(['user', 'setting', 'shop', 'tickets'])
const icon = ref('menu')

const menusList = ref([])
const initMenuList = async () => {
  menusList.value = await menuList()
  console.log(menusList.value)
}
initMenuList()
const defaultActive = ref(sessionStorage.getItem('path') || '/users')

const savePath = (path) => {
  sessionStorage.setItem('path', `/${path}`)
  defaultActive.value = path
}
</script>

<style lang="scss" scoped></style>
