<template>
  <el-card>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-input
          :placeholder="$t('table.placeholder')"
          clearable
          v-model="queryForm.query"
        ></el-input>
      </el-col>
      <el-button type="primary" :icon="Search" @click="initGetUsersList">
        {{ $t('table.search') }}
      </el-button>
      <el-button type="primary" @click.prevent="handleDialogValue()">
        {{ $t('table.adduser') }}
      </el-button>
    </el-row>
  </el-card>
  <el-card>
    <el-table :data="tableData" stripe style="width: 100%">
      <!-- highlight-current-row="true" -->
      <el-table-column
        :prop="item.prop"
        :label="$t(`table.${item.label}`)"
        v-for="(item, index) in options"
        :key="index"
        :min-width="item.width"
        align="center"
        :sortable="item.sortable"
      >
        <template #default="{ row }" v-if="item.prop === 'action'">
          <el-button
            type="primary"
            size="small"
            :icon="Edit"
            @click="handleDialogValue(row)"
          ></el-button>
          <el-button
            type="danger"
            size="small"
            :icon="Delete"
            @click="deleteUser(row)"
          ></el-button>
          <!-- <el-button
            type="success"
            size="small"
            :icon="InfoFilled"
            @click="getUserDetails(row)"
          ></el-button> -->
        </template>
      </el-table-column>
    </el-table>
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
import { Search, Edit, Delete } from '@element-plus/icons-vue'
import { getUsers, getUser, delUser } from '@/api/users'
import { options } from './options'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useI18n } from 'vue-i18n'
import Dialog from './components/dialog'
// import { isNull } from '@/utils/filters'

const i18n = useI18n()

const typeAdd = 0
const typeEdit = 1

const deleteUser = (row) => {
  ElMessageBox.confirm(i18n.t('dialog.deleteTitle'), 'Warning', {
    confirmButtonText: i18n.t('dialog.confirm'),
    cancelButtonText: i18n.t('dialog.cancel'),
    type: 'warning'
  })
    .then(async () => {
      await delUser(row.no)
      initGetUsersList()
      ElMessage({
        type: 'success',
        message: i18n.t('message.delSuccess')
      })
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: i18n.t('message.delCancel')
      })
    })
}

// const getUserDetails = (row) => {
//   handleDialogValue(row)
// }

const queryForm = ref({
  query: '',
  pagenum: 1,
  pagesize: 5
})

const dialogVisible = ref(false)

const dialogType = ref(0)

const dialogTable = ref({})
// 0: 添加用户 1: 编辑用户

const handleDialogValue = async (row) => {
  // console.log(111, row)
  if (!row) {
    dialogType.value = typeAdd
    dialogTable.value = { gender: '男', password: '123456' }
  } else {
    dialogType.value = typeEdit
    dialogTable.value = await getUser({ no: row.no })
  }
  dialogVisible.value = true
  // console.log(222, dialogType.value)
}

const tableData = ref([])
const total = ref(0)

const initGetUsersList = async () => {
  const res = await getUsers(queryForm.value)
  // console.log(res)
  tableData.value = res.users
  total.value = res.total
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
