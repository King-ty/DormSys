<template>
  <el-dialog
    :model-value="dialogVisible"
    :title="dialogTitle"
    width="40%"
    @close="handleClose"
  >
    <el-form ref="formRef" :model="form" label-width="15%" :rules="rules">
      <!-- 记得国际化! -->
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
import { defineEmits, defineProps, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { addUser, editUser } from '@/api/users'
import i18n from '@/i18n'
import formRules from '@/utils/formRules'

const typeAdd = 0
const typeEdit = 1

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
  no: formRules.addNo,
  name: formRules.name,
  password: formRules.password,
  gender: formRules.gender,
  email: formRules.email,
  tel: formRules.tel,
  // major: formRules.major,
  grade: formRules.grade,
  classno: formRules.classno
})
</script>

<style lang="scss" scoped></style>
