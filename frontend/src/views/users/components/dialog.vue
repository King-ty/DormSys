<template>
  <el-dialog
    :model-value="dialogVisible"
    :title="dialogTitle"
    width="40%"
    @close="handleClose"
  >
    <el-form ref="formRef" :model="form" label-width="15%" :rules="rules">
      <el-form-item :label="$t('table.no')" prop="no">
        <el-input v-model="form.no" :disabled="props.dialogType === typeEdit" />
      </el-form-item>
      <el-form-item :label="$t('table.name')" prop="name">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item
        :label="$t('table.password')"
        prop="password"
        v-if="props.dialogType === typeAdd"
      >
        <el-input v-model="form.password" show-password prop="password" />
      </el-form-item>
      <el-form-item :label="$t('table.building')" prop="building">
        <el-select
          v-model="form.building_id"
          :placeholder="$t('dialog.selectBuilding')"
          filterable
          default-first-option
        >
          <!-- {{ form.building_id }} -->
          <el-option
            v-for="(item, index) in buildingSelectList"
            :key="index"
            :label="item.name"
            :value="item.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item :label="$t('table.dormitory')" prop="dormitory">
        <el-select
          v-model="form.dormitory_id"
          :placeholder="$t('dialog.selectDormitory')"
          filterable
          default-first-option
        >
          <el-option
            v-for="(item, index) in dormitorySelectList"
            :key="index"
            :label="item.no"
            :value="item.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item :label="$t('table.gender')" prop="gender">
        <el-radio-group v-model="form.gender">
          <el-radio-button label="男">
            {{ $t('table.male') }}
          </el-radio-button>
          <el-radio-button label="女">{{ $t('table.female') }}</el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item :label="$t('table.tel')" prop="tel">
        <el-input v-model="form.tel" />
      </el-form-item>
      <el-form-item :label="$t('table.email')" prop="email">
        <el-input v-model="form.email" />
      </el-form-item>
      <el-form-item :label="$t('table.major')" prop="major">
        <el-input v-model="form.major" />
      </el-form-item>
      <el-form-item :label="$t('table.grade')" prop="grade">
        <el-input v-model="form.grade" />
      </el-form-item>
      <el-form-item :label="$t('table.classno')" prop="classno">
        <el-input v-model.number="form.classno" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">
          {{ $t('dialog.cancel') }}
        </el-button>
        <el-button type="primary" @click="handleConfirm">
          {{ $t('dialog.confirm') }}
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { defineEmits, defineProps, ref, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { addUser, editUser } from '@/api/users'
import { getBuildingSelects } from '@/api/buildings'
import { getDormitorySelects } from '@/api/dormitories'
import i18n from '@/i18n'
import formRules from '@/utils/formRules'

const typeAdd = 0
const typeEdit = 1

const form = ref({
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
  grade: '',
  classno: ''
})

const buildingSelectList = ref([])
const dormitorySelectList = ref([])

onMounted(async () => {
  const res = await getBuildingSelects()
  buildingSelectList.value = res.buildings
  // console.log(buildingSelectList.value)
})

watch(
  () => form.value.building_id,
  async () => {
    // console.log('###123')
    const res = await getDormitorySelects(form.value.building_id)
    dormitorySelectList.value = res.dorms
    // console.log(res)
  },
  { deep: true }
)

const props = defineProps({
  dialogType: {
    type: Number,
    default: 0,
    required: true
  },
  dialogVisible: {
    type: Boolean,
    default: false
    // required: true
  },
  dialogTable: {
    type: Object,
    default: () => {}
  }
})

const dialogTitle = ref('')

watch(
  () => props.dialogType,
  () => {
    // console.log('###', props.dialogType)
    dialogTitle.value =
      props.dialogType === typeAdd
        ? i18n.global.t('dialog.addUserTitle')
        : i18n.global.t('dialog.editUserTitle')
  },
  { deep: true }
)

const emits = defineEmits(['update:modelValue', 'getUsersList'])

const handleClose = () => {
  emits('update:modelValue', false)
}

const formRef = ref(null)
const handleConfirm = async () => {
  await formRef.value.validate(async (valid, fields) => {
    if (valid) {
      if (props.dialogType === typeAdd) {
        await addUser(form.value)
        ElMessage({
          message: i18n.global.t('message.addSuccess'),
          type: 'success'
        })
      } else {
        await editUser(form.value)
        ElMessage({
          message: i18n.global.t('message.updeteSuccess'),
          type: 'success'
        })
      }

      emits('getUsersList')
      handleClose()
    } else {
      console.log('error submit!', fields)
    }
  })
}

watch(
  () => props.dialogTable,
  () => {
    // console.log(1, props.dialogTable)
    form.value = props.dialogTable
  },
  { deep: true }
)

const rules = ref({
  no: formRules.addNo,
  name: formRules.name,
  password: formRules.password,
  // gender: formRules.gender,
  email: formRules.email,
  tel: formRules.tel,
  // major: formRules.major,
  grade: formRules.grade,
  classno: formRules.classno
})
</script>

<style lang="scss" scoped></style>
