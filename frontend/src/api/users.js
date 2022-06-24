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
    url: prefix + 'user',
    method: 'put',
    data
  })
}

export const delUser = (id) => {
  // 删除有点特殊！
  return request({
    url: prefix + `user/${id}`,
    method: 'delete'
  })
}

export const getUser = (params) => {
  return request({
    url: prefix + 'user',
    method: 'get',
    params
  })
}
