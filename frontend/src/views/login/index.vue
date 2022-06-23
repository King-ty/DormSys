<template>
  <div class="login-container">
    <el-form ref="ruleFormRef" :model="form" :rules="rules" class="login-form">
      <div class="title-container">
        <h3 class="title">{{ $t('login.title') }}</h3>
      </div>

      <el-form-item prop="no">
        <svg-icon icon="user" class="svg-container"></svg-icon>
        <el-input v-model="form.no" :placeholder="$t('login.noPlace')" />
      </el-form-item>

      <el-form-item prop="password">
        <svg-icon icon="password" class="svg-container"></svg-icon>
        <el-input
          v-model="form.password"
          :placeholder="$t('login.passwordPlace')"
          type="password"
          show-password
        />
        <!-- <svg-icon
          :icon="passwordType === 'password' ? 'eye' : 'eye-open'"
          @click="changeType"
        ></svg-icon> -->
      </el-form-item>
      <el-button
        type="primary"
        class="login-button"
        @click="handleLogin(ruleFormRef)"
      >
        {{ $t('login.btnTitle') }}
      </el-button>

      <a
        href="forget-password"
        @click.prevent="handleForgetPassword"
        class="click-link"
      >
        忘记密码？
      </a>
    </el-form>
    <Dialog v-model="dialogVisible" :no="form.no"></Dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import { passwordVeriCode } from '@/api/login'
import { useI18n } from 'vue-i18n'
import Dialog from './components/dialog'

const i18n = useI18n()

const store = useStore()

const form = ref({
  no: '1950001',
  password: '123456'
})

const rules = ref({
  // TODO:国际化+限定内容检查
  no: [
    {
      required: true,
      message: 'Please input Activity username',
      trigger: 'blur'
    }
  ],
  password: [
    {
      required: true,
      message: 'Please input Activity password',
      trigger: 'blur'
    }
  ]
})

const ruleFormRef = ref()
const handleLogin = async (formEl) => {
  // console.log(formEl)
  if (!formEl) return
  await formEl.validate(async (valid, fields) => {
    if (valid) {
      store.dispatch('app/login', form.value)
    } else {
      console.log('error submit!', fields)
    }
  })
}

const dialogVisible = ref(false)

const handleForgetPassword = async () => {
  await ruleFormRef.value.validateField('no', async (error) => {
    if (!error) {
      dialogVisible.value = true
      await passwordVeriCode(form.value.no)
      ElMessage({
        type: 'success',
        message: i18n.t('message.codeSuccess')
      })
    } else {
      console.log('error no!')
    }
  })
}

// const passwordType = ref('password')
// const changeType = () => {
//   if (passwordType.value === 'password') {
//     passwordType.value = 'text'
//   } else {
//     passwordType.value = 'password'
//   }
// }
</script>

<style lang="scss" scoped>
$bg: #2d3a4b;
$dark_gray: #889aa4;
$light_gray: #eee;
$cursor: #fff;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;

    ::v-deep .el-form-item {
      border: 1px solid rgba(255, 255, 255, 0.1);
      background: rgba(0, 0, 0, 0.1);
      border-radius: 5px;
      color: #454545;
    }

    ::v-deep .el-input {
      display: inline-block;
      height: 47px;
      width: 92%;

      input {
        background: transparent;
        border: 0px;
        -webkit-appearance: none;
        border-radius: 0px;
        padding: 12px 5px 12px 15px;
        color: $light_gray;
        height: 47px;
        caret-color: $cursor;
      }
    }
    .login-button {
      width: 100%;
      box-sizing: border-box;
    }
  }

  .tips {
    font-size: 16px;
    line-height: 28px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }

    ::v-deep .lang-select {
      position: absolute;
      top: 4px;
      right: 0;
      background-color: white;
      font-size: 22px;
      padding: 4px;
      border-radius: 4px;
      cursor: pointer;
    }
  }
  .click-link {
    padding: 16px;
    text-align: right;
    display: block;
    color: $light_gray;
    &:hover {
      color: $dark_gray;
    }
  }
}
</style>
