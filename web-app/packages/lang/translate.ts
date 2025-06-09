import EN from './translations/EN.js'
import PL from './translations/PL.js'

const returnTranslation = (lang: string, key: string) => {
  if (lang === 'PL') {
    return PL[key]
  } else {
    return EN[key]
  }
}

export default returnTranslation