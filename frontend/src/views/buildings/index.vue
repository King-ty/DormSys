<template>
  <el-card>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-input
          :placeholder="$t('table.searchHolder')"
          clearable
          v-model="queryForm.query"
        ></el-input>
      </el-col>
      <el-button type="primary" :icon="Search" @click="initGetBuildingsList">
        {{ $t('table.search') }}
      </el-button>
      <el-button type="primary" @click.prevent="handleDialogValue()">
        {{ $t('table.addBuilding') }}
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
        <template
          v-slot="{ row }"
          v-if="
            item.prop === 'is_bed_on_table' ||
            item.prop === 'is_independent_bathroom'
          "
        >
          <el-icon v-if="row[item.prop]"><Check /></el-icon>
          <el-icon v-else><Close /></el-icon>
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
    @getBuildingsList="initGetBuildingsList"
  ></Dialog>
  <!-- v-if="dialogVisible" -->
</template>

<script setup>
import { ref } from 'vue'
import { Search, Edit, Check, Close } from '@element-plus/icons-vue'
import { getBuildings } from '@/api/buildings'
import { options } from './options'
import Dialog from './components/dialog'
// import { useI18n } from 'vue-i18n'

const queryForm = ref({
  query: '',
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
    dialogTable.value = {
      gender: '男',
      is_bed_on_table: false,
      is_independent_bathroom: false
    }
  } else {
    dialogType.value = typeEdit
    dialogTable.value = JSON.parse(JSON.stringify(row))
  }
  dialogVisible.value = true
  // console.log(222, dialogType.value)
}

const tableData = ref([])
const total = ref(0)

const initGetBuildingsList = async () => {
  const res = await getBuildings(queryForm.value)
  // console.log(res)
  tableData.value = res.buildings
  total.value = res.total
}
initGetBuildingsList()

const handleSizeChange = (pageSize) => {
  queryForm.value.pagenum = 1
  queryForm.value.pageSize = pageSize
  initGetBuildingsList()
}

const handleCurrentChange = (pageNum) => {
  queryForm.value.pagenum = pageNum
  initGetBuildingsList()
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

.building-select {
  padding-left: 10px;
  padding-right: 10px;
}
</style>
