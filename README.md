# Owlet Custom Integration

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]

[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]

A custom component for the Owlet smart sock

## Installation

1. Use [HACS](https://hacs.xyz/docs/use/download/download/), in `HACS > Integrations > Explore & Add Repositories` search for "Owlet".
2. Restart Home Assistant.
3. [![Add Integration][add-integration-badge]][add-integration] or in the HA UI go to "Settings" -> "Devices & Services" then click "+" and search for "Owlet Smart Sock".


<!---->

## Usage

The `Owlet` integration offers integration with the Owlet Smart Sock cloud service. This provides sensors such as heart rate, oxygen saturation, charge percentage.

This integration provides the following entities:

- Binary sensors - charging status, high heart rate alert, low heart rate alert, high oxygen alert, low oxygen alert, low battery alert, lost power alert, sock diconnected alert, and sock status.
- Sensors - battery level, oxygen saturation, oxygen saturation 10 minute average, heart rate, battery time remaining, signal strength, and skin temperature.

## Options

- Seconds between polling - Number of seconds between each call for data from the owlet cloud service, default is 5 seconds.

---

[commits-shield]: https://img.shields.io/github/commit-activity/w/ryanbdclark/owlet?style=for-the-badge
[commits]: https://github.com/ryanbdclark/owlet/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license]: LICENSE
[license-shield]: https://img.shields.io/github/license/ryanbdclark/owlet.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Ryan%20Clark%20%40ryanbdclark-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/ryanbdclark/owlet.svg?style=for-the-badge
[releases]: https://github.com/ryanbdclark/owlet/releases
[user_profile]: https://github.com/ryanbdclark
[add-integration]: https://my.home-assistant.io/redirect/config_flow_start?domain=owlet
[add-integration-badge]: https://my.home-assistant.io/badges/config_flow_start.svg
