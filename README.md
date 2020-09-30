# Notice

The component and platforms in this repository are not meant to be used by a
user, but as a "victorsmartkill" that custom component developers can build
upon, to make more awesome stuff.

HAVE FUN! 😎

## Why?

This is simple, by having custom_components look (README + structure) the same
it is easier for developers to help each other and for users to start using them.

If you are a developer and you want to add things to this "victorsmartkill" that you think more
developers will have use for, please open a PR to add it :)

## What?

This repository contains multiple files, here is a overview:

| File                                                 | Purpose                                                                                                                                             |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `.devcontainer/*`                                    | Used for development/testing with VSCODE, more info in the readme file in that dir.                                                                 |
| `.github/ISSUE_TEMPLATE/feature_request.md`          | Template for Feature Requests                                                                                                                       |
| `.github/ISSUE_TEMPLATE/issue.md`                    | Template for issues                                                                                                                                 |
| `.github/settings.yml`                               | Probot settings to control the repository settings.                                                                                                 |
| `.vscode/tasks.json`                                 | Tasks for the devcontainer.                                                                                                                         |
| `custom_components/victorsmartkill/.translations/*`  | [Translation files.](https://developers.home-assistant.io/docs/en/next/internationalization_custom_component_localization.html#translation-strings) |
| `custom_components/victorsmartkill/__init__.py`      | The component file for the integration.                                                                                                             |
| `custom_components/victorsmartkill/binary_sensor.py` | Binary sensor platform for the integration.                                                                                                         |
| `custom_components/victorsmartkill/config_flow.py`   | Config flow file, this adds the UI configuration possibilities.                                                                                     |
| `custom_components/victorsmartkill/const.py`         | A file to hold shared variables/constants for the entire integration.                                                                               |
| `custom_components/victorsmartkill/manifest.json`    | A [manifest file](https://developers.home-assistant.io/docs/en/creating_integration_manifest.html) for Home Assistant.                              |
| `custom_components/victorsmartkill/sensor.py`        | Sensor platform for the integration.                                                                                                                |
| `custom_components/victorsmartkill/switch.py`        | Switch sensor platform for the integration.                                                                                                         |
| `CONTRIBUTING.md`                                    | Guidelines on how to contribute.                                                                                                                    |
| `example.png`                                        | Screenshot that demonstrate how it might look in the UI.                                                                                            |
| `LICENSE`                                            | The license file for the project.                                                                                                                   |
| `README.md`                                          | The file you are reading now, should contain info about the integration, installation and configuration instructions.                               |
| `requirements.txt`                                   | Python packages used by this integration.                                                                                                           |

## How?

If you want to use all the potential and features of this victorsmartkill tempalte you
should use Visual Studio Code to develop in a container. In this container you
will have all the tools to ease your python development and a dedicated Home
Assistant core instance to run your integration. See `.devcontainer/README.md` for more information.

If you need to work on the python library in parallel of this integration
(`sampleclient` in this example) there are different options. The following one seems
easy to implement:

- Create a dedicated branch for your python library on a public git repository
- Update in the `manifest.json` file the `requirements` key to point on your development branch
- Each time you need to make a modification to your python library, push it to your
  development branch and increase the number of the python library version in `manifest.json` file
  to ensure Home Assistant update the code of the python library. (example `"requirements": ["git+https://...==0.0.1beta2"]`).

---

README content if this was a published component:

---

# victorsmartkill

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

_Component to integrate with [victorsmartkill][victorsmartkill]._

**This component will set up the following platforms.**

| Platform        | Description                         |
| --------------- | ----------------------------------- |
| `binary_sensor` | Show something `True` or `False`.   |
| `sensor`        | Show info from victorsmartkill API. |
| `switch`        | Switch something `True` or `False`. |

![example][exampleimg]

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `victorsmartkill`.
4. Download _all_ the files from the `custom_components/victorsmartkill/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Victor Smart Kill"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/victorsmartkill/.translations/en.json
custom_components/victorsmartkill/.translations/nb.json
custom_components/victorsmartkill/.translations/sensor.nb.json
custom_components/victorsmartkill/__init__.py
custom_components/victorsmartkill/binary_sensor.py
custom_components/victorsmartkill/config_flow.py
custom_components/victorsmartkill/const.py
custom_components/victorsmartkill/manifest.json
custom_components/victorsmartkill/sensor.py
custom_components/victorsmartkill/switch.py
```

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

---

[victorsmartkill]: https://github.com/toreamun/victorsmartkill-homeassistant
[buymecoffee]: https://www.buymeacoffee.com/toreamun
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/toreamun/victorsmartkill-homeassistant/victorsmartkill.svg?style=for-the-badge
[commits]: https://github.com/toreamun/victorsmartkill-homeassistant/commits/master
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/custom-components/victorsmartkill.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Tore%20Amundsen%20%40toreamun-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/toreamun/victorsmartkill-homeassistant/victorsmartkill.svg?style=for-the-badge
[releases]: https://github.com/toreamun/victorsmartkill-homeassistant/releases
