# КАТ България - HACS интеграция за Home Assistant

![Downloads](https://img.shields.io/github/downloads/nedevski/hass_kat_bulgaria/latest/total?style=flat-square)
![Last release](https://img.shields.io/github/release-date/nedevski/hacs_kat_bulgaria?style=flat-square)
![Code size](https://img.shields.io/github/languages/code-size/nedevski/hacs_kat_bulgaria?style=flat-square)
[![Quality Gate](https://img.shields.io/sonar/quality_gate/Nedevski_hass_kat_bulgaria?server=https%3A%2F%2Fsonarcloud.io&style=flat-square)](https://sonarcloud.io/summary/overall?id=Nedevski_hass_kat_bulgaria&branch=main)
[![Code coverage](https://img.shields.io/sonar/coverage/Nedevski_hass_kat_bulgaria?server=https%3A%2F%2Fsonarcloud.io&style=flat-square)](https://sonarcloud.io/component_measures?id=Nedevski_hass_kat_bulgaria&metric=coverage&view=list)

Тази интеграция позволява да се следят наличните глоби към КАТ България. Интеграцията взима информацията директно от официалния сайт на КАТ ([e-uslugi.mvr.bg](https://e-uslugi.mvr.bg/services/kat-obligations)) без да логва абсолютно нищо. Единственото място на което се пазят данните е локално, като конфигурация на интеграцията.

![Config flow](https://raw.githubusercontent.com/Nedevski/hass_kat_bulgaria/main/images/screenshots-bg.png)

## Инсталиране

Тъй като това е неофициална интеграция е необходимо първо да се [инсталира HACS](https://hacs.xyz/docs/setup/download) - разширението за сваляне на неофициални интеграции към Home Assistant.

След това изпозлвайте търсачката за намиране на интеграцията "KAT Bulgaria" или използвайте бутона по-долу

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Nedevski&repository=hass_kat_bulgaria&category=integration)

**След сваляне трябва да се рестартира Home Assistant за да е видима интеграцията в списъка!**

След рестарт се добавя като нормална интеграция: Настройки => Устройства и услуги => Добавяне на интеграция => KAT Bulgaria.

## Как работи

Интеграцията поддържа както физически, така и юридически лица.

- За физически лица проверката се извършва по ЕГН + лична карта/шофьорска книжка/номер на автомобил
- За юридически лица са нужни ЕГН и лична карта на собственика, както и БУЛСТАТ на фирмата
  За да настроите интеграцията, трябва да дадете име на човек, неговото ЕГН, както и номера на шофьорската му книжка.

За всеки конфигуриран човек се създават няколко entities, които се обновяват на всеки 2 часа:

- Общ брой глоби ([сензор, int](https://www.home-assistant.io/integrations/sensor/))
- Брой връчени глоби ([сензор, int](https://www.home-assistant.io/integrations/sensor/))
- Брой невръчени глоби ([сензор, int](https://www.home-assistant.io/integrations/sensor/))
- Налични глоби? ([бинарен сензор](https://www.home-assistant.io/integrations/binary_sensor/))
- Невръчени глоби? ([бинарен сензор](https://www.home-assistant.io/integrations/binary_sensor/))
- Обща дължима сума ([сензор, int](https://www.home-assistant.io/integrations/sensor/)) - взима предвид активните отстъпки

## Превод на Български език

За да работят преводите правилно, трябва и езика на системата, и езика на потребителя да са зададени на Български.

## Python библиотека

Тази интеграция използва моята Python библиотека - [py_kat_bulgaria](https://github.com/Nedevski/py_kat_bulgaria).

Библиотеката е изцяло независима от тази интеграция и може да се използва самостоятелно. Повече информация има в нейното `README.md`.

---

Ако харесвате работата ми, почерпете ме с 1 бира в Ko-Fi:

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/nedevski/tip)

---

## KAT Bulgaria - a HACS integration for Home Assistant

The KAT Bulgaria custom integration allows users to check if they have any new fines from the Bulgarian Traffic Police (KAT). The integration is a wrapper around the official government website ([e-uslugi.mvr.bg](https://e-uslugi.mvr.bg/services/kat-obligations)).

![Config flow](https://raw.githubusercontent.com/Nedevski/hass_kat_bulgaria/main/images/screenshots-en.png)

## Installation

Since this is an unofficial integration, you have to download the [HACS (Home Assistant Community Store)](https://hacs.xyz/docs/setup/download).

After installing it you will have a link to HASS on the left menu. There you can search for **"KAT Bulgaria"**, open the integration and click Download.

**You have to restart Home Assistant in order to be able to see the integration!**

After restarting you add the integration as usual: Settings => Devices and services => Add integration => KAT Bulgaria.

## How it works

The integrations supports checks for both individuals and businesses

- For individuals you need a combination of EGN (Unified Civil Number) and Driving License Number/National ID Number/Car Plate Number
- For businesses you need the EGN and National ID Number of the owner, as well as the BULSTAT of the company

For each configured instance, a couple of entities are created and updated every 2 hours:

- Count Non-Served ([sensor, int](https://www.home-assistant.io/integrations/sensor/)) - total count of non-served fines
- Count Served ([sensor, int](https://www.home-assistant.io/integrations/sensor/)) - total count of non-served fines
- Count Total ([sensor, int](https://www.home-assistant.io/integrations/sensor/)) - total count of existing fines
- Has Non-Served Tickets ([binary_sensor](https://www.home-assistant.io/integrations/binary_sensor/))
- Has Tickets ([binary_sensor](https://www.home-assistant.io/integrations/binary_sensor/))
- Total BGN Owed ([sensor, int](https://www.home-assistant.io/integrations/sensor/)) - the total sum that needs to be paid, which takes into account the active discounts for early payment

## Standalone Python library

The integration uses my [py_kat_bulgaria](https://github.com/Nedevski/py_kat_bulgaria) library.

It's entirely separate from this integration and can be used on its own. Check out its description for more information.

---

If you like my work - consider supporting me:

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/nedevski/tip)
