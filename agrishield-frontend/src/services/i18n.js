import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// Translations
const resources = {
  en: {
    translation: {
      'dashboard.title': 'Flood Risk Dashboard',
      'risk.low': 'Low Risk',
      'report.button': 'Report Flood Sign'
    }
  },
  sw: {
    translation: {
      'dashboard.title': 'Dashibodi ya Hatari ya Mafuriko',
      'risk.low': 'Hatari Ndogo',
      'report.button': 'Ripoti Ishara ya Mafuriko'
    }
  }
};

i18n.use(initReactI18next).init({
  resources,
  lng: 'en',
  fallbackLng: 'en',
  interpolation: {
    escapeValue: false
  }
});

export default i18n;