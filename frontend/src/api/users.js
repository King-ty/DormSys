import request from './request'

const prefix = 'user/'

export const getUsers = (params) => {
  return request({ url: prefix + 'get-users', params })
}

export const addUser = (data) => {
  return request({
    url: prefix + 'user',
    method: 'post',
    data
  })
}

export const editUser = (data) => {
  return request({
    url: `users/${data.id}`,
    method: 'put',
    data
  })
}

export const delUser = (id) => {
  return request({
    url: `users/${id}`,
    method: 'delete'
  })
}
