import request from './request'

const prefix = 'dormitory/'

export const getDormitorySelects = (buildingId) => {
  return request({
    url: prefix + 'get-dormitorySelects',
    params: {
      building_id: buildingId
    }
  })
}
