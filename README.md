# Victor Smart-Kill

Home Assistant integration for Victor Smart-Kill WI-FI electronic mouse and rat traps from [VictorPest.com]. This integration is open source and not made by VictorPest.com.

<img src="https://play-lh.googleusercontent.com/tfSd-O7Qwc8p8kYzTbJlDlq-nZzUyRHCMEvM87155kTtwEpVP7iNMgNzg2gWujjZ0jmq=s360-rw" width="128" alt="Victor logo">

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

- Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
- If you do not have a `custom_components` directory (folder) there, you need to create it.
- Change dircetory to `custom_components`.
- Download lastest version 

```
wget https://github.com/toreamun/victorsmartkill-homeassistant/releases/latest/download/victorsmartkill.zip
```

- Unzip victorsmartkill.zip into folder victorsmartkill

```
unzip victorsmartkill.zip -d victorsmartkill       
```

- Delete victorsmartkill.zip

```
rm victorsmartkill.zip
```

- Restart Home Assistant
- Tøm nettleseren sin cache. Hvis du ikke gjør dette risikerer du å ikke finne integrasjonen i listen av tilgjengelige integrasjoner.

- Place the files you downloaded in the new directory (folder) you created.
- Restart Home Assistant
- In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Victor Smart-Kill"

# Trap models and versions
This integration should work with traps that use the VictorPest app. Please create an [issue](https://github.com/toreamun/victorsmartkill-homeassistant/issues/new/choose) if you have trouble with your trap.

It is very helpfull if you can check the [list of models](https://github.com/toreamun/victorsmartkill-homeassistant/wiki/Hardware) and update the list if you have an unlisted trap or version.



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
