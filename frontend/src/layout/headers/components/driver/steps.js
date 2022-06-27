export const steps = (t) => [
  {
    element: '#guide',
    popover: {
      title: t('driver.guideBtn'),
      description: '引导功能图标按钮',
      position: 'left'
    }
  },
  {
    element: '#hamburger',
    popover: {
      title: t('driver.hamburgerBtn'),
      description: '菜单折叠按钮',
      position: 'bottom'
    }
  },
  {
    element: '#screenFull',
    popover: {
      title: t('driver.fullScreen'),
      description: '全屏按钮',
      position: 'left'
    }
  }
]
