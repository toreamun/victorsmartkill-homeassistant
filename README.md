# Victor Smart-Kill

Home Assistant integration for Victor Smart-Kill WI-FI electronic mouse and rat traps from [VictorPest.com]. This integration is open source and not made by VictorPest.com.

<img src="https://play-lh.googleusercontent.com/tfSd-O7Qwc8p8kYzTbJlDlq-nZzUyRHCMEvM87155kTtwEpVP7iNMgNzg2gWujjZ0jmq=s360-rw" width="128" alt="Victor logo">

[![GitHub Release][releases-shield]][releases]
[![Language grade: Python][language-grade-shield]][lgtm-project]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

![image-m1-mouse-trap](https://user-images.githubusercontent.com/12134766/154821889-45f78843-bcd3-4d67-844a-5767fb0709b4.png)
![image-m2-rat-trap](https://user-images.githubusercontent.com/12134766/154821879-3a3fffeb-964d-4a06-9b65-866c8e4cfb6a.png)

![example][exampleimg]

## Dowload the integration
### HACS download (alternative 1)

The easiest way to add the integration to your Homeassistant installation is using [HACS]. I you have HACS installed:
1. Goto HACS -> integrations (http://homeassistant.local:8123/hacs/integrations) and select "explore and download repositories".
2. Search for Victor Smart-Kill, and select to download the repository.
3. Restart Home Assistant (http://homeassistant.local:8123/config/server_control and select restart).


### Script download (alternative 2)

You need some kind of terminal to use this method. You can use one of the SSH add-ons from the [Add-on Store](https://my.home-assistant.io/redirect/_change/?redirect=supervisor_store%2) if you run HassOS. 

1. Open terminal. Change directory to your Home Assistant configuration directory (where you find `configuration.yaml`) if you are not using HassOS.
2. Run this script

```
wget -O - https://raw.githubusercontent.com/toreamun/victorsmartkill-homeassistant/master/get | bash -
```

3. Restart Home Assistant (http://homeassistant.local:8123/config/server_control and select restart)
4. Before the integration can show up in the list of integrations, you need to clear your browser cache or perform hard-refresh.

### Manual download (alternative 3)

You need some kind of terminal to use this method. You can use one of the SSH add-ons from the Add-on Store if you run HassOS.

1. Open terminal and change to the directory for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory there, you need to create it.
3. Change dircetory to `custom_components`.
4. Download lastest version 

```
wget https://github.com/toreamun/victorsmartkill-homeassistant/releases/latest/download/victorsmartkill.zip
```

5. Unzip victorsmartkill.zip into folder victorsmartkill

```
unzip victorsmartkill.zip -d victorsmartkill       
```

6. Delete victorsmartkill.zip

```
rm victorsmartkill.zip
```

7. Restart Home Assistant (http://homeassistant.local:8123/config/server_control and select restart)
8. Before the integration can show up in the list of integrations, you need to clear your browser cache or perform hard-refresh.

## Install the integration

Once the integration has been downloaded and Home Assistant has been restarted, go to Configuration -> Integrations (http://homeassistant.local:8123/config/integrations) and click the + to select Victor Smart-Kill and add the new integration. **You  may have to clear your browser cache or perform hard-refresh if the integrations is missing from the list.** Check the [log](http://homeassistant.local:8123/config/logs) if you still have problems.


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
