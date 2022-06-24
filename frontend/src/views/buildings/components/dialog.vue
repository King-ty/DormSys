<template>
  <el-dialog
    :model-value="dialogVisible"
    :title="dialogTitle"
    width="40%"
    @close="handleClose"
  >
    <el-form ref="formRef" :model="form" label-width="15%" :rules="rules">
      <el-form-item :label="$t('table.buildingName')" prop="name">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item :label="$t('table.gender')" prop="gender">
        <el-radio-group v-model="form.gender">
          <el-radio-button label="男">
            {{ $t('table.male') }}
          </el-radio-button>
          <el-radio-button label="女">{{ $t('table.female') }}</el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item :label="$t('table.is_bed_on_table')" prop="is_bed_on_table">
        <el-switch v-model="form.is_bed_on_table" />
      </el-form-item>
      <el-form-item
        :label="$t('table.is_independent_bathroom')"
        prop="is_independent_bathroom"
      >
        <el-switch v-model="form.is_independent_bathroom" />
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
import { defineEmits, defineProps, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { addUser, editUser } from '@/api/users'
import i18n from '@/i18n'
import formRules from '@/utils/formRules'

const typeAdd = 0
// const typeEdit = 1

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

const emits = defineEmits(['update:modelValue', 'getBuildingsList'])

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

      emits('getBuildingsList')
      handleClose()
    } else {
      console.log('error submit!', fields)
    }
  })
}

const form = ref({
  no: '',
  name: '',
  password: '',
  gender: '',
  email: '',
  tel: '',
  major: '',
  grade: '',
  classno: ''
})

watch(
  () => props.dialogTable,
  () => {
    // console.log(1, props.dialogTable)
    form.value = props.dialogTable
  },
  { deep: true }
)

const rules = ref({
  name: formRules.name
})
</script>

<style lang="scss" scoped></style>
