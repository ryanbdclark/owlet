# Owlet Custom Integration

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]

[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]

A custom component for the Owlet smart sock, currently this only supports the owlet smart sock 3.

If you have a smart sock 2 and would like to contribute then please do so.

## Installation

1. Use [HACS](https://hacs.xyz/docs/setup/download), in `HACS > Integrations > Explore & Add Repositories` search for "Owlet". After adding this `https://github.com/RyanClark123/owlet` as a custom repository.
2. Restart Home Assistant.
3. [![Add Integration][add-integration-badge]][add-integration] or in the HA UI go to "Settings" -> "Devices & Services" then click "+" and search for "Owlet Smart Sock".


<!---->

## Usage

The `Owlet` integration offers integration with the Owlet Smart Sock cloud service. This provides sensors such as heart rate, oxygen saturation, charge percentage.

This integration provides the following entities:

- Binary sensors - charging status, high heart rate alert, low heart rate alert, high oxygen alert, low oxygen alert, low battery alert, lost power alert, sock diconnected alert, and sock status.
- Sensors - battery level, oxygen saturation, oxygen saturation 10 minute average, heart rate, battery time remaining, signal strength, and skin temperature.

## Options

- Seconds between polling - Number of seconds between each call for data from the owlet cloud service, default is 10 seconds.

---

[commits-shield]: https://img.shields.io/github/commit-activity/w/RyanClark123/owlet?style=for-the-badge
[commits]: https://github.com/RyanClark123/owlet/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license]: LICENSE
[license-shield]: https://img.shields.io/github/license/RyanClark123/owlet.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Ryan%20Clark%20%40RyanClark123-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/RyanClark123/owlet.svg?style=for-the-badge
[releases]: https://github.com/RyanClark123/owlet/releases
[user_profile]: https://github.com/RyanClark123
[add-integration]: https://my.home-assistant.io/redirect/config_flow_start?domain=owlet
[add-integration-badge]: https://my.home-assistant.io/badges/config_flow_start.svg