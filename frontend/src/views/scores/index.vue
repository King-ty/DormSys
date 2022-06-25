<template>
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
        :sortable="
          item.prop === 'time' ||
          item.prop === 'dormitory' ||
          item.prop === 'score'
        "
      >
        <template v-slot="{ row }" v-if="item.prop === 'check_type'">
          {{ $t(`type.check_${checkSelectList[row.check_type].name}`) }}
        </template>
        <template v-slot="{ row }" v-else-if="item.prop === 'time'">
          {{ $filters.filterTime(row.time, 'YYYY-MM-DD HH:mm:ss') }}
        </template>
        <template #default="{ row }" v-else-if="item.prop === 'action'">
          <el-button
            type="danger"
            size="small"
            :icon="Delete"
            @click="deleteScore(row)"
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
</template>

<script setup>
import { ref } from 'vue'
import { Delete } from '@element-plus/icons-vue'
import { getScores, delScore } from '@/api/scores'
import { options, checkSelectList } from './options'
// import Dialog from './components/dialog'
import { useI18n } from 'vue-i18n'
import { ElMessageBox, ElMessage } from 'element-plus'

const i18n = useI18n()

const queryForm = ref({
  query: '',
  pagenum: 1,
  pagesize: 5
})

const tableData = ref([])
const total = ref(0)

const initGetScoresList = async () => {
  const res = await getScores(queryForm.value)
  // console.log(res)
  tableData.value = res.scores
  total.value = res.total
}
initGetScoresList()

const handleSizeChange = (pageSize) => {
  queryForm.value.pagenum = 1
  queryForm.value.pageSize = pageSize
  initGetScoresList()
}

const handleCurrentChange = (pageNum) => {
  queryForm.value.pagenum = pageNum
  initGetScoresList()
}

const deleteScore = (row) => {
  ElMessageBox.confirm(i18n.t('dialog.deleteTitle'), 'Warning', {
    confirmButtonText: i18n.t('dialog.confirm'),
    cancelButtonText: i18n.t('dialog.cancel'),
    type: 'warning'
  })
    .then(async () => {
      await delScore(row.id)
      initGetScoresList()
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
