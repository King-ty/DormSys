import request from './request'

const prefix = 'score/'

export const getScores = (params) => {
  return request({
    url: prefix + 'get-scores',
    params
  })
}

export const addScore = (data) => {
  return request({
    url: prefix + 'score',
    method: 'post',
    data
  })
}

export const delScore = (id) => {
  return request({
    url: prefix + `score/${id}`,
    method: 'delete'
  })
}
