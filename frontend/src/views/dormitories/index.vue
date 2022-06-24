<template>
  <el-card>
    <el-row :gutter="20"> </el-row>
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
      >
        <template v-slot="{ row }" v-if="item.prop === 'stu_num'">
          {{ `${row.num} / ${row.max_num}` }}
        </template>
        <template v-slot="{ row }" v-else-if="item.prop === 'students'">
          <el-link
            v-for="(it, index) in row.students"
            :key="index"
            type="primary"
          >
            {{ it.no }} {{ it.name }}
            <template v-if="index !== row.students.length - 1">
              ,&nbsp;
            </template>
          </el-link>
        </template>
        <template #default="{ row }" v-else-if="item.prop === 'action'">
          <el-button
            type="primary"
            size="small"
            :icon="Edit"
            @click="handleDialogValue(row)"
          ></el-button>
          <!-- <el-button type="success" size="small" :icon="InfoFilled"></el-button> -->
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
import { Edit } from '@element-plus/icons-vue'
import { getDormitories } from '@/api/dormitories'
import { options } from './options'
// import { useI18n } from 'vue-i18n'
import Dialog from './components/dialog'
// import { isNull } from '@/utils/filters'

// const i18n = useI18n()

const queryForm = ref({
  building_id: 0,
  pagenum: 1,
  pagesize: 5
})

const dialogVisible = ref(false)

const dialogType = ref(0)

const dialogTable = ref({})

const typeAdd = 0
const typeEdit = 1
// 0: 添加用户 1: 编辑用户

const handleDialogValue = (row) => {
  // console.log(111, row)
  if (!row) {
    dialogType.value = typeAdd
    dialogTable.value = { gender: '男', password: '123456' }
  } else {
    dialogType.value = typeEdit
    dialogTable.value = JSON.parse(JSON.stringify(row))
  }
  dialogVisible.value = true
  // console.log(222, dialogType.value)
}

const tableData = ref([])
const total = ref(0)

const initGetDormitoriesList = async () => {
  const res = await getDormitories(queryForm.value)
  // console.log(res)
  tableData.value = res.dorms
  total.value = res.total
}
initGetDormitoriesList()

const handleSizeChange = (pageSize) => {
  queryForm.value.pagenum = 1
  queryForm.value.pageSize = pageSize
  initGetDormitoriesList()
}

const handleCurrentChange = (pageNum) => {
  queryForm.value.pagenum = pageNum
  initGetDormitoriesList()
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
