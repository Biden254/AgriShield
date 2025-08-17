// Language switching functionality
document.addEventListener('DOMContentLoaded', function() {
    const languageToggle = document.getElementById('languageToggle');
    const mobileLanguageToggle = document.getElementById('mobileLanguageToggle');
    let currentLanguage = 'en';

    // Translations dictionary
    const translations = {
        en: {
            'auth.login_title': 'Login to AgriShield',
            'auth.email_label': 'Email',
            'auth.email_placeholder': 'Enter your email',
            'auth.password_label': 'Password',
            'auth.password_placeholder': 'Enter your password',
            'auth.login_button': 'Login',
            'auth.no_account': "Don't have an account?",
            'auth.signup_button': 'Sign Up',
            'auth.signup_title': 'Create Account',
            'auth.full_name_label': 'Full Name',
            'auth.full_name_placeholder': 'Enter your full name',
            'auth.phone_label': 'Phone Number',
            'auth.phone_placeholder': 'Enter your phone number',
            'auth.confirm_password_label': 'Confirm Password',
            'auth.confirm_password_placeholder': 'Re-enter your password',
            'auth.user_type_label': 'I am a:',
            'auth.farmer_option': 'Farmer',
            'auth.fisher_option': 'Fisher',
            'auth.official_option': 'Government Official',
            'auth.have_account': 'Already have an account?',
            'nav.home': 'Home',
            'nav.alerts': 'Alerts',
            'nav.predictions': 'Predictions',
            'nav.report': 'Report',
            'hero.title': 'Protect Your Farm with Early Flood Warnings',
            'hero.subtitle': 'Combining satellite data and local knowledge for Budalang\'i farmers',
            'hero.cta_primary': 'View Predictions',
            'hero.cta_secondary': 'Report Signs',
            'risk.title': 'Current Flood Risk',
            'risk.high': 'HIGH RISK',
            'risk.high_description': 'Flood expected in 2-3 days. Take immediate action.',
            'map.title': 'Flood Risk Map',
            'alerts.title': 'Recent Alerts',
            'alerts.high_title': 'High Flood Risk',
            'alerts.time_ago': '2 hours ago',
            'alerts.high_message': 'River Nzoia rising rapidly. Expected to flood in 48 hours.',
            'alerts.moderate_title': 'Moderate Risk',
            'alerts.moderate_message': 'Heavy rains upstream detected. Prepare your farm.',
            'alerts.action': 'Recommended Actions',
            'visualization.title': 'Flood Predictions & Historical Data',
            'visualization.timeline_title': '5-Day Flood Risk Forecast',
            'visualization.legend_scientific': 'Scientific Data',
            'visualization.legend_indigenous': 'Community Reports',
            'visualization.historical_title': 'Historical Flood Events',
            'report.title': 'Report Flood Indicators',
            'report.type_label': 'Indicator Type',
            'report.select_default': 'Select an indicator',
            'report.type_river': 'River Color Change',
            'report.type_bird': 'Bird Behavior',
            'report.type_plants': 'Water Plants Movement',
            'report.location_label': 'Location',
            'report.location_placeholder': 'E.g. Near Bunyala market',
            'report.description_label': 'Description',
            'report.description_placeholder': 'Describe what you observed...',
            'report.submit': 'Submit Report',
            'footer.about': 'About',
            'footer.contact': 'Contact',
            'footer.privacy': 'Privacy',
            'footer.copyright': '© 2025 AgriShield. All rights reserved.'
        },
        sw: {
            'auth.login_title': 'Ingia kwenye AgriShield',
            'auth.email_label': 'Barua Pepe',
            'auth.email_placeholder': 'Weka barua pepe yako',
            'auth.password_label': 'Nenosiri',
            'auth.password_placeholder': 'Weka nenosiri lako',
            'auth.login_button': 'Ingia',
            'auth.no_account': 'Huna akaunti?',
            'auth.signup_button': 'Jisajili',
            'auth.signup_title': 'Fungua Akaunti',
            'auth.full_name_label': 'Jina Kamili',
            'auth.full_name_placeholder': 'Weka jina lako kamili',
            'auth.phone_label': 'Nambari ya Simu',
            'auth.phone_placeholder': 'Weka nambari yako ya simu',
            'auth.confirm_password_label': 'Thibitisha Nenosiri',
            'auth.confirm_password_placeholder': 'Weka tena nenosiri lako',
            'auth.user_type_label': 'Mimi ni:',
            'auth.farmer_option': 'Mkulima',
            'auth.fisher_option': 'Mvuvi',
            'auth.official_option': 'Afisa wa Serikali',
            'auth.have_account': 'Tayari una akaunti?',
            'nav.home': 'Nyumbani',
            'nav.alerts': 'Taadhari',
            'nav.predictions': 'Utabiri',
            'nav.report': 'Ripoti',
            'hero.title': 'Linda Shamba Lako Kwa Tahadhari Za Mafuriko Mapema',
            'hero.subtitle': 'Kuchanganya data za satelaiti na ujuzi wa kienyeji kwa wakulima wa Budalangi',
            'hero.cta_primary': 'Tazama Utabiri',
            'hero.cta_secondary': 'Ripoti Ishara',
            'risk.title': 'Hatari Ya Mafuriko Ya Sasa',
            'risk.high': 'HATARI KUBWA',
            'risk.high_description': 'Mafuriko yanatarajiwa kwa siku 2-3. Chukua hatua mara moja.',
            'map.title': 'Ramani Ya Hatari Ya Mafuriko',
            'alerts.title': 'Taadhari Za Hivi Karibuni',
            'alerts.high_title': 'Hatari Kubwa Ya Mafuriko',
            'alerts.time_ago': 'Masaa 2 yaliyopita',
            'alerts.high_message': 'Mto Nzoia unaongezeka kwa kasi. Unatarajiwa kufurika kwa masaa 48.',
            'alerts.moderate_title': 'Hatari Ya Wastani',
            'alerts.moderate_message': 'Mvua nyingi zimegunduliwa mkondo wa juu. Jiandae shambani.',
            'alerts.action': 'Hatua Zilizopendekezwa',
            'visualization.title': 'Utabiri Wa Mafuriko Na Data Ya Kihistoria',
            'visualization.timeline_title': 'Utabiri Wa Hatari Ya Mafuriko Kwa Siku 5',
            'visualization.legend_scientific': 'Data Ya Kisayansi',
            'visualization.legend_indigenous': 'Ripoti Za Jamii',
            'visualization.historical_title': 'Matukio Ya Mafuriko Ya Kihistoria',
            'report.title': 'Ripoti Ishara Za Mafuriko',
            'report.type_label': 'Aina Ya Ishara',
            'report.select_default': 'Chagua ishara',
            'report.type_river': 'Mabadiliko Ya Rangi Ya Mto',
            'report.type_bird': 'Tabia Ya Ndege',
            'report.type_plants': 'Msukosuko Wa Mimea Ya Majini',
            'report.location_label': 'Mahali',
            'report.location_placeholder': 'Mf. Karibu na soko la Bunyala',
            'report.description_label': 'Maelezo',
            'report.description_placeholder': 'Eleza ulichoona...',
            'report.submit': 'Wasilisha Ripoti',
            'footer.about': 'Kuhusu',
            'footer.contact': 'Mawasiliano',
            'footer.privacy': 'Faragha',
            'footer.copyright': '© 2025 AgriShield. Haki zote zimehifadhiwa.'
        }
    };

    // Function to update all translatable elements
    function updateLanguage(lang) {
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            if (translations[lang][key]) {
                element.textContent = translations[lang][key];
            }
        });

        // Update placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
            const key = element.getAttribute('data-i18n-placeholder');
            if (translations[lang][key]) {
                element.setAttribute('placeholder', translations[lang][key]);
            }
        });

        // Update language toggle buttons
        document.querySelectorAll('.en-text').forEach(el => {
            el.style.display = lang === 'en' ? 'none' : 'inline';
        });
        document.querySelectorAll('.sw-text').forEach(el => {
            el.style.display = lang === 'sw' ? 'none' : 'inline';
        });

        // Update HTML lang attribute
        document.documentElement.lang = lang;
        currentLanguage = lang;
    }

    // Toggle language
    function toggleLanguage() {
        const newLanguage = currentLanguage === 'en' ? 'sw' : 'en';
        updateLanguage(newLanguage);
    }

    // Event listeners
    languageToggle.addEventListener('click', toggleLanguage);
    mobileLanguageToggle.addEventListener('click', toggleLanguage);

    // Initialize with English
    updateLanguage('en');
});