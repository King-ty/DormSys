<template>
  <el-dialog
    :model-value="dialogVisible"
    :title="dialogTitle"
    width="40%"
    @close="handleClose"
  >
    <el-form ref="formRef" :model="form" label-width="15%" :rules="rules">
      <!-- 记得国际化! -->
      <el-form-item :label="$t(`dialog.username`)" prop="username">
        <el-input v-model="form.username" />
      </el-form-item>
      <el-form-item
        :label="$t(`dialog.password`)"
        prop="password"
        v-if="dialogTitle === '添加用户'"
      >
        <el-input v-model="form.password" show-password prop="password" />
      </el-form-item>
      <el-form-item :label="$t(`dialog.email`)" prop="email">
        <el-input v-model="form.email" />
      </el-form-item>
      <el-form-item :label="$t(`dialog.mobile`)" prop="mobile">
        <el-input v-model="form.mobile" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">{{ $t(dialogTable.cancel) }}</el-button>
        <el-button type="primary" @click="handleConfirm">
          {{ $t(dialogTable.confirm) }}
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

const props = defineProps({
  dialogTitle: {
    type: String,
    default: '',
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

const emits = defineEmits(['update:modelValue', 'getUsersList'])

const handleClose = () => {
  emits('update:modelValue', false)
}

const formRef = ref(null)
const handleConfirm = async () => {
  await formRef.value.validate(async (valid, fields) => {
    if (valid) {
      props.dialogTitle === '添加用户'
        ? await addUser(form.value)
        : await editUser(form.value)
      ElMessage({
        message: i18n.global.t('message.updeteSuccess'),
        type: 'success'
      })
      emits('getUsersList')
      handleClose()
    } else {
      console.log('error submit!', fields)
    }
  })
}

const form = ref({
  password: '',
  email: '',
  mobile: ''
})

watch(
  () => props.dialogTable,
  () => {
    console.log(1, props.dialogTable)
    form.value = props.dialogTable
  },
  { deep: true }
)

const rules = ref({
  username: [
    { required: true, message: 'Please input Activity name', trigger: 'blur' },
    { min: 2, max: 10, message: 'Length should be 3 to 5', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Please input Activity name', trigger: 'blur' },
    { min: 3, max: 16, message: 'Length should be 3 to 5', trigger: 'blur' }
  ],
  email: [
    { required: true, message: 'Please input Activity name', trigger: 'blur' },
    {
      type: 'email',
      message: 'Please input correct email address',
      trigger: ['blur', 'change']
    }
  ],
  mobile: [
    { required: true, message: 'Please input Activity name', trigger: 'blur' }
  ]
})
</script>

<style lang="scss" scoped></style>
