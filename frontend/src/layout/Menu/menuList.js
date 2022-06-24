export const menuList = [
  {
    authName: '用户管理',
    path: 'users',
    children: [
      {
        authName: '用户列表',
        path: 'users',
        children: [],
        order: 1
      }
    ],
    order: 1
  },
  {
    authName: '宿舍管理',
    path: 'dormitories',
    children: [
      {
        authName: '宿舍列表',
        path: 'dormitories',
        children: [],
        order: 1
      }
    ],
    order: 2
  }
]
