<template>
  <el-dialog
    :model-value="dialogVisible"
    :title="dialogTitle"
    width="40%"
    @close="handleClose"
  >
    <el-form ref="formRef" :model="form" label-width="15%" :rules="rules">
      <!-- 记得国际化! -->
      <el-form-item :label="$t(`dialog.vericode`)" prop="vericode">
        <el-input show-password v-model="form.vericode" />
      </el-form-item>
      <el-form-item :label="$t(`dialog.newPassword`)" prop="password">
        <el-input v-model="form.password" show-password />
      </el-form-item>
      <el-form-item :label="$t(`dialog.confirmPassword`)" prop="password2">
        <el-input v-model="password2" show-password />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">{{ $t('dialog.cancel') }}</el-button>
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
import { resetPassword } from '@/api/login'
import i18n from '@/i18n'

const props = defineProps({
  dialogVisible: {
    type: Boolean,
    default: false
    // required: true
  },
  no: {
    type: String,
    required: true
  }
})

const emits = defineEmits(['update:modelValue'])

const handleClose = () => {
  emits('update:modelValue', false)
}

const formRef = ref(null)
const form = ref({
  no: props.no,
  vericode: '',
  password: ''
})
const password2 = ref('')

const handleConfirm = async () => {
  await formRef.value.validate(async (valid, fields) => {
    if (valid) {
      await resetPassword(form.value)
      ElMessage({
        message: i18n.global.t('message.updeteSuccess'),
        type: 'success'
      })
      handleClose()
    } else {
      console.log('error submit!', fields)
    }
  })
}

watch(
  () => props.no,
  () => {
    form.value.no = props.no
  }
)

const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
    // password 是表单上绑定的字段
  } else if (value !== form.value.password) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

const rules = ref({
  vericode: [
    { required: true, message: 'Please input Activity name', trigger: 'blur' },
    { min: 6, max: 6, message: 'Length should be 6', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Please input password', trigger: 'blur' },
    { min: 3, max: 16, message: 'Length should be 3 to 16', trigger: 'blur' }
  ],
  password2: [
    {
      required: true,
      validator: validatePass2,
      trigger: 'blur'
    },
    { min: 3, max: 16, message: 'Length should be 3 to 16', trigger: 'blur' }
  ]
})
</script>

<style lang="scss" scoped></style>
