import { createI18n } from 'vue-i18n'
import EN from './lang/en'
import ZH from './lang/zh'

const messages = {
  en: {
    ...EN
  },
  zh: {
    ...ZH
  }
}

const getCurLang = () => {
  const UAlang = navigator.language
  const langCode = UAlang.indexOf('zh') !== -1 ? 'zh' : 'en'
  localStorage.setItem('lang', langCode)
  return langCode
}

const i18n = createI18n({
  legacy: false,
  globalInjection: true,
  locale: getCurLang() || 'zh',
  messages: messages
})

export default i18n
