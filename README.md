# Victor Smart-Kill

Home Assistant integration for Victor Smart-Kill WI-FI electronic mouse and rat traps from [VictorPest.com].

![Victor logo][victor-logo]

[![GitHub Release][releases-shield]][releases]
[![Language grade: Python][language-grade-shield]][lgtm-project]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

![example][exampleimg]

## HACS installation

The easiest way to add this to your Homeassistant installation is using [HACS]. Once installed from HACS UI, go to Configuration -> Integrations and click the + to select Victor Smart-Kill and add the new integration.

## Manual installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `victorsmartkill`.
4. Download _all_ the files from the `custom_components/victorsmartkill/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Victor Smart-Kill"

---

[victorpest.com]: https://www.victorpest.com/
[buymecoffee]: https://www.buymeacoffee.com/toreamun
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg
[license-shield]: https://img.shields.io/github/license/toreamun/victor-smart-kill
[maintenance-shield]: https://img.shields.io/badge/maintainer-Tore%20Amundsen%20%40toreamun-blue.svg
[releases-shield]: https://img.shields.io/github/release/toreamun/victorsmartkill-homeassistant
[releases]: https://github.com/toreamun/victorsmartkill-homeassistant/releases
[language-grade-shield]: https://img.shields.io/lgtm/grade/python/g/toreamun/victorsmartkill-homeassistant.svg?logo=lgtm&logoWidth=18
[lgtm-project]: https://lgtm.com/projects/g/toreamun/victorsmartkill-homeassistant/context:python
[hacs]: https://github.com/custom-components/hacs
[exampleimg]: https://raw.githubusercontent.com/toreamun/victorsmartkill-homeassistant/master/example.png
[victor-logo]: https://static.victorpest.com/skin/frontend/rwd/vpus/images/vpus-logo.jpg
