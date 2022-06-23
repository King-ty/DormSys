import request from './request'

export const login = (data) => {
  return request({
    url: '/user/login',
    method: 'POST',
    data
  })
}

export const passwordVeriCode = (no) => {
  return request({
    url: '/user/password-vericode',
    params: {
      no
    }
  })
}

export const resetPassword = (data) => {
  return request({
    url: '/user/reset-password',
    method: 'post',
    data
  })
}
