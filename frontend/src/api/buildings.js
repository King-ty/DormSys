import request from './request'

const prefix = 'building/'

export const getBuildingSelects = (params) => {
  return request({ url: prefix + 'get-buildingSelects', params })
}

export const getBuildings = (params) => {
  return request({ url: prefix + 'get-buildings', params })
}
