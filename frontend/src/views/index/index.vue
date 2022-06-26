<template>
  <el-card>
    <el-avatar shape="square" :size="avatarSize" :src="avatarUrl" />
  </el-card>
  <el-card>
    <!-- 通知 -->
  </el-card>
  <el-pagination
    v-model:currentPage="queryForm.pagenum"
    v-model:page-size="queryForm.pagesize"
    :page-sizes="[5, 10, 15, 20]"
    background
    layout="total, sizes, prev, pager, next, jumper"
    :total="total"
    @size-change="handleSizeChange"
    @current-change="handleCurrentChange"
    class="el-pagination"
  />
  <Dialog
    v-model="dialogVisible"
    :dialogType="dialogType"
    :dialogTable="dialogTable"
    @getUsersList="initGetUsersList"
  ></Dialog>
  <!-- v-if="dialogVisible" -->
</template>

<script setup>
import { ref } from 'vue'
// import { Search, Edit } from '@element-plus/icons-vue'
// import { getUsers, getUser } from '@/api/users'
// import { ElMessage, ElMessageBox } from 'element-plus'
// import { useI18n } from 'vue-i18n'
import Dialog from './components/dialog'
// import { isNull } from '@/utils/filters'

// const i18n = useI18n()

const queryForm = ref({
  query: '',
  pagenum: 1,
  pagesize: 5
})

const dialogVisible = ref(false)

const dialogTable = ref({})
// 0: 添加用户 1: 编辑用户

// const handleDialogValue = async (row) => {
//   // console.log(111, row)
//   if (!row) {
//     dialogType.value = typeAdd
//     dialogTable.value = { gender: '男', password: '123456' }
//   } else {
//     dialogType.value = typeEdit
//     dialogTable.value = await getUser({ no: row.no })
//   }
//   dialogVisible.value = true
//   // console.log(222, dialogType.value)
// }

// const tableData = ref([])
const total = ref(0)

const initGetUsersList = async () => {
  // const res = await getUsers(queryForm.value)
  // console.log(res)
  // tableData.value = res.users
  // total.value = res.total
}
initGetUsersList()

const handleSizeChange = (pageSize) => {
  queryForm.value.pagenum = 1
  queryForm.value.pageSize = pageSize
  initGetUsersList()
}

const handleCurrentChange = (pageNum) => {
  queryForm.value.pagenum = pageNum
  initGetUsersList()
}
</script>

<style lang="scss" scoped>
::v-deep .el-input__suffix {
  align-items: center;
}

.el-pagination {
  padding: 16px;
  text-align: center;
  // margin-top: 20px;
}
</style>
