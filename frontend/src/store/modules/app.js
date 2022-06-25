import { login as loginApi } from '@/api/login'
import router from '@/router'

export default {
  namespaced: true, // 这里注意不要漏掉d！！
  state: () => ({
    token: localStorage.getItem('token') || '',
    role: localStorage.getItem('role') || 2,
    no: localStorage.getItem('no') || -1,
    siderType: true,
    lang: localStorage.getItem('lang') || 'zh'
  }),
  mutations: {
    setToken(state, token) {
      state.token = token
      localStorage.setItem('token', token)
    },
    setRole(state, role) {
      state.role = role
      localStorage.setItem('role', role)
    },
    setNo(state, no) {
      state.no = no
      localStorage.setItem('no', no)
    },
    changeSiderType(state) {
      state.siderType = !state.siderType
    },
    changeLang(state, lang) {
      state.lang = lang
    }
  },
  actions: {
    login({ commit }, userInfo) {
      return new Promise((resolve, reject) => {
        loginApi(userInfo)
          .then((res) => {
            // console.log(res)
            commit('setToken', res.token)
            commit('setRole', res.role)
            commit('setNo', userInfo.no)
            router.replace('/')
            resolve()
          })
          .catch((err) => {
            reject(err)
          })
      })
    },
    logout({ commit }) {
      commit('setToken', '')
      localStorage.clear()
      router.replace('/login')
    }
  }
}
