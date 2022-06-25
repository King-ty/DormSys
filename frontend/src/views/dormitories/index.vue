<template>
  <el-card>
    <el-row :gutter="20">
      <el-select
        class="building-select"
        v-model="queryForm.building_id"
        :placeholder="$t('dialog.selectBuilding')"
        filterable
        default-first-option
      >
        <el-option
          v-for="(item, index) in buildingSelectList"
          :key="index"
          :label="item.name"
          :value="item.id"
        />
      </el-select>
      <el-button type="primary" :icon="Search" @click="initGetDormitoriesList">
        {{ $t('table.screen') }}
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
            @click="handleDialogValue(row)"
          >
            {{ $t('table.score') }}
          </el-button>
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
    :dialogTable="dialogTable"
    @getDormitoriesList="initGetDormitoriesList"
  ></Dialog>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { getDormitories } from '@/api/dormitories'
import { getBuildingSelects } from '@/api/buildings'
import { options } from './options'
import store from '@/store'
import Dialog from './components/dialog'
// import { useI18n } from 'vue-i18n'

// const i18n = useI18n()

const dialogVisible = ref(false)
const dialogTable = ref({})

const handleDialogValue = (row) => {
  dialogTable.value = {
    dorm_id: row.id,
    work_no: store.getters.no,
    check_type: 1
  }
  dialogVisible.value = true
  // console.log(222, dialogType.value)
}

const buildingSelectList = ref([])
onMounted(async () => {
  const res = await getBuildingSelects()
  buildingSelectList.value = res.buildings
  // console.log(buildingSelectList.value)
})

const queryForm = ref({
  building_id: null,
  pagenum: 1,
  pagesize: 5
})

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

.building-select {
  padding-left: 10px;
  padding-right: 10px;
}
</style>
