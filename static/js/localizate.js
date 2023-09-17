// обработка языковой панели

const locale = 'ru';

let translations = {};

document.addEventListener('DOMContentLoaded', () => {
    setLocale(locale);
});

const setLocale = async (newLocale) => {
    translations = await fetchTranslations(newLocale);
    translatePage();
};

const fetchTranslations = async (newLocale) => {
    const response = await fetch(`/static/lang/${newLocale}.json`);
    return await response.json();
};

const translatePage = () => {
    document.querySelectorAll('[lang-key]').forEach((element) => {
        let key = element.getAttribute('lang-key');
        let translation = translations[key];
        element.innerText = translation;
    });
};

const localizationSwitcher = document.getElementById('localization-switcher');
localizationSwitcher.addEventListener('change', (event) => {
    const newLocale = event.target.value;
    setLocale(newLocale);
});

