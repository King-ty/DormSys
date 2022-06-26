<template>
  <el-card>
    <el-row :gutter="10" align="middle">
      <el-col :span="3" align="middle">
        <el-avatar shape="square" :size="100" :src="avatarUrl" /><br />
        <el-button
          type="primary"
          size="small"
          :icon="Edit"
          @click="handleDialogValue()"
        ></el-button>
      </el-col>
      <el-col :span="1" />
      <el-col :span="7">
        <div v-for="(item, index) in options" :key="index">
          <template
            v-if="$store.getters.role == 2 || showInfo.includes(item.prop)"
          >
            {{ $t(`table.${item.label}`) }}:&nbsp;
            <template v-if="item.prop === 'role'">
              {{ $t(`role.${roles[userInfo[item.prop]]}`) }}
            </template>
            <template v-else>
              {{ userInfo[item.prop] }}
            </template>
          </template>
        </div>
      </el-col>
    </el-row>
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
    :dialogTable="dialogTable"
    @getUsersList="initGetUsersList"
  ></Dialog>
  <!-- v-if="dialogVisible" -->
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Edit } from '@element-plus/icons-vue'
import { getUser } from '@/api/users'
import { options, roles } from './options'
// import { ElMessage, ElMessageBox } from 'element-plus'
// import { useI18n } from 'vue-i18n'
import Dialog from './components/dialog'
import { useStore } from 'vuex'
// import { isNull } from '@/utils/filters'

// const i18n = useI18n()

const store = useStore()

const avatarUrl = ref(
  'https://ts1.cn.mm.bing.net/th/id/R-C.86a0fa17b9b37ff7518b552e2517a0ae?rik=CX0%2fMchuLIBQVA&riu=http%3a%2f%2fimg.crcz.com%2fallimg%2f201809%2f11%2f1536666825645562.jpg&ehk=g6IGr0cDabvrRd5KSQdbup2trGpltKDfA7Hx7eopcm0%3d&risl=&pid=ImgRaw&r=0&sres=1&sresct=1'
)

const userInfo = ref({
  no: '',
  name: '',
  password: '',
  building: '',
  building_id: 0,
  dormitory: '',
  dormitory_id: 0,
  gender: '',
  email: '',
  tel: '',
  major: '',
  grade: 2019,
  classno: ''
})

const showInfo = ref([
  'no',
  'name',
  'building',
  'gender',
  'tel',
  'email',
  'role'
])

onMounted(async () => {
  userInfo.value = await getUser({ no: store.getters.no })
  console.log(userInfo)
})

const queryForm = ref({
  query: '',
  pagenum: 1,
  pagesize: 5
})

const dialogVisible = ref(false)

const dialogTable = ref({})

const handleDialogValue = async (row) => {
  dialogTable.value = userInfo.value
  dialogVisible.value = true
  // console.log(222, dialogType.value)
}

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
