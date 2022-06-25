import request from './request'

const prefix = 'score/'

export const addScore = (data) => {
  return request({
    url: prefix + 'score',
    method: 'post',
    data
  })
}

export const getScores = (params) => {
  return request({
    url: prefix + 'get-scores',
    params
  })
}
