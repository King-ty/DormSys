import request from './request'

const prefix = 'building/'

export const getBuildingSelects = (params) => {
  return request({ url: prefix + 'get-buildingSelects', params })
}

export const getBuildings = (params) => {
  return request({ url: prefix + 'get-buildings', params })
}

export const addBuilding = (data) => {
  return request({ url: prefix + 'building', method: 'post', data })
}

export const editBuilding = (data) => {
  return request({ url: prefix + 'building', method: 'put', data })
}
