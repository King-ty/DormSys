<template>
  <el-dialog
    :model-value="dialogVisible"
    :title="dialogTitle"
    width="40%"
    @close="handleClose"
  >
    <el-form ref="formRef" :model="form" label-width="15%" :rules="rules">
      <el-form-item :label="$t('table.score_n')" prop="score">
        <el-input v-model.number="form.score" />
      </el-form-item>
      <el-form-item :label="$t('table.score_n')" prop="score">
        <el-select
          class="building-select"
          v-model="form.check_type"
          :placeholder="$t('table.check_type')"
          filterable
          default-first-option
        >
          <el-option
            v-for="(item, index) in checkSelectList"
            :key="index"
            :label="$t(`type.check_${item.name}`)"
            :value="item.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item :label="$t('table.profile')" prop="score">
        <el-input v-model="form.profile" type="textarea" />
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
import i18n from '@/i18n'
import formRules from '@/utils/formRules'
import { checkSelectList } from './options'
import { addScore } from '@/api/score'

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

const dialogTitle = ref('')

const emits = defineEmits(['update:modelValue', 'getDormitoriesList'])

const handleClose = () => {
  emits('update:modelValue', false)
}

const form = ref({
  dorm_id: -1,
  work_no: '',
  time: 0,
  score: 100,
  check_type: 0,
  profile: ''
})

const formRef = ref(null)
const handleConfirm = async () => {
  await formRef.value.validate(async (valid, fields) => {
    if (valid) {
      form.value.time = new Date().getTime()
      console.log(form.value.time)
      await addScore(form.value)
      ElMessage({
        message: i18n.global.t('message.addSuccess'),
        type: 'success'
      })

      emits('getDormitoriesList')
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

const validateScore = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入得分'))
    // password 是表单上绑定的字段
  } else if (value < 0 || value > 100) {
    callback(new Error('得分应在1~100之间'))
  } else {
    callback()
  }
}

const rules = ref({
  name: formRules.name,
  score: [
    {
      required: true,
      validator: validateScore,
      trigger: 'blur'
    }
  ]
})
</script>

<style lang="scss" scoped></style>
