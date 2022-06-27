<template>
  <el-dialog
    :model-value="dialogVisible"
    :title="dialogTitle"
    width="60%"
    @close="handleClose"
  >
    <!-- <el-form ref="formRef" :model="form" label-width="15%" :rules="rules">
      <el-form-item :label="$t('table.no')" prop="no">
        <el-input v-model="form.no" disabled />
      </el-form-item>
      <el-form-item :label="$t('table.name')" prop="name">
        <el-input v-model="form.name" disabled />
      </el-form-item>
      <el-form-item :label="$t('table.tel')" prop="tel">
        <el-input v-model="form.tel" />
      </el-form-item>
      <el-form-item :label="$t('table.email')" prop="email">
        <el-input v-model="form.email" />
      </el-form-item>
    </el-form> -->
    <wang-editor></wang-editor>
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
import { editUser } from '@/api/users'
import i18n from '@/i18n'
import WangEditor from '@/components/wangEditor'

const form = ref({
  no: '',
  name: '',
  email: '',
  tel: ''
})

const props = defineProps({
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

const dialogTitle = i18n.global.t('dialog.editInfoTitle')

const emits = defineEmits(['update:modelValue', 'getUserInfo'])

const handleClose = () => {
  emits('update:modelValue', false)
}

const formRef = ref(null)
const handleConfirm = async () => {
  await formRef.value.validate(async (valid, fields) => {
    if (valid) {
      await editUser(form.value)
      ElMessage({
        message: i18n.global.t('message.updeteSuccess'),
        type: 'success'
      })
      emits('getUsersList')
      handleClose()
    } else {
      console.log('error submit!', fields)
      ElMessage({
        message: i18n.global.t('message.formInvalid'),
        type: 'error'
      })
    }
  })
}

watch(
  () => props.dialogTable,
  () => {
    // console.log(1, props.dialogTable)
    form.value = props.dialogTable
    // form.value.grade = parseInt(form.value.grade)
  },
  { deep: true }
)

// const rules = ref({
//   email: formRules.email,
//   tel: formRules.tel
// })
</script>

<style lang="scss" scoped></style>
