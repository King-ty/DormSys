import request from './request'

const prefix = 'dormitory/'

export const addScore = (data) => {
  return request({
    url: prefix + 'score',
    method: 'post',
    data
  })
}
