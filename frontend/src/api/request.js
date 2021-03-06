import axios from 'axios'
import { ElMessage } from 'element-plus'
import store from '@/store'
import i18n from '@/i18n'

const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API,
  timeout: 5000
})

service.interceptors.request.use(
  (config) => {
    config.headers.Authorization = store.getters.token
    return config
  },
  (error) => {
    return Promise.reject(new Error(error))
  }
)

service.interceptors.response.use(
  (response) => {
    // console.log('response', response)
    const { meta, data } = response.data
    if (meta.code === '00') {
      return data
    } else {
      ElMessage.error(meta.msg)
      return Promise.reject(new Error(meta.msg || 'Error'))
      // .catch((err) => {
      //   console.log(err)
      // })
    }
  },
  (error) => {
    if (error.response.status === 401) {
      // console.log(store)
      ElMessage.info(i18n.global.t('login.expired'))
      return store.dispatch('app/logout')
    }
    error.response && ElMessage.error(error.response.data)
    return Promise.reject(new Error(error.response.data)) // 这样没有问题吗？？
  }
)

export default service
