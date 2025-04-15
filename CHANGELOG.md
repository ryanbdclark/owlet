# Changelog

<!--next-version-placeholder-->
## 2025.4.3 (2025-04-15)
### Fix
* Bumping pyowletapi to 2025.4.8.
* Changes to how the sensors are stored to solve the issue where only one device is added, thanks [`@MarjovanLier`](https://github.com/MarjovanLier). ([`1244bff`](https://github.com/ryanbdclark/owlet/commit/1244bffcb48d7337a9d7a0da518959fe4b31a230))

## 2025.4.2 (2025-04-14)
### Fix
* Bumping pyowletapi to 2025.4.1, should hopefully stop issue where only one device was added to HA. ([`d323cbf`](https://github.com/ryanbdclark/owlet/commit/d323cbfd11411ff34866ead492de10c109c72689))

## 2025.4.1 (2025-04-11)
### Fix
* Changes to stop errors after refactoring pyowletapi ([`6b343a7`](https://github.com/ryanbdclark/owlet/commit/6b343a76caad3375e10c80f4d26942a1bbbb831d))

## 2025.4.0 (2025-04-11)
### Fix
* Bumping pyowletapi to 2025.4.0 ([`268365c`](https://github.com/ryanbdclark/owlet/commit/268365ccd428418dd5707f0569ce738b54a12fdd))

## 2024.10.1 (2024-10-09)
### Feature
* Base station has now been removed from binary sensors and added as a switch ([`f63e0a6`](https://github.com/ryanbdclark/owlet/commit/f63e0a6dfeab1a05ba09ef3e0087cb404ba0dac4))
### Fix
* Bump pyowletapi to 2024.10.1 ([`82823be`](https://github.com/ryanbdclark/owlet/commit/82823be1c8265d2b9431771136853febef648650))
* Fix strings for password and connection error in all languages ([`14787e0`](https://github.com/ryanbdclark/owlet/commit/14787e03c4d275f46f446921a3ee133fc7cfd1b1))
* Add state class to battery minutes and O2 saturation 10 minute average ([`0991eb3`](https://github.com/ryanbdclark/owlet/commit/0991eb31d919f3ee9f65ece793166d7ee3e33c38))

## 2024.9.1 (2024-09-26)
### Feature
* Now includes French translation, thanks [`@Julien80`](https://github.com/Julien80) ([`f3c853e`](https://github.com/ryanbdclark/owlet/commit/f3c853e2d7243d766889f2d18c718819da30e4be))

## 2024.6.1 (2024-06-17)
### Fix
* Bumping pyowletapi to 2024.6.1 to resolve setup errors ([`52710ba`](https://github.com/ryanbdclark/owlet/commit/52710ba7de53fd07195537c2a5fd2f95bc7dfd1a))

## 2024.5.1 (2024-05-13)
### Feature
* As per HA core patterns, certain sensors will now show as unavailable when sock is charging ([`ceade24`](https://github.com/ryanbdclark/owlet/commit/ceade24851479b8c9bc60b7b8bed74a7bdb927e9))
* Oxygen 10 minute average now only shows a figure if it is between 0 and 100 this avoids skewing by 255 values before the 10 minutes is reached, thanks @coreywillwhat ([`5e17ecd`](https://github.com/ryanbdclark/owlet/commit/5e17ecdeb2aca5bbb35f19ca5795a2c5e0f776ab))
### Fix
* Refactoring as per core maintainers suggestions ([`ceade24`](https://github.com/ryanbdclark/owlet/commit/ceade24851479b8c9bc60b7b8bed74a7bdb927e9))


## 2024.3.1
### Feature
* Base station on added as binary sensor ([`50c55dc`](https://github.com/ryanbdclark/owlet/commit/50c55dcfd30d15027155a8f1d05340238501522d))

### Fix
* Bumping pyowletapi to 2024.3.2 ([`50c55dc`](https://github.com/ryanbdclark/owlet/commit/50c55dcfd30d15027155a8f1d05340238501522d))
* UI config now allows you to set interval to 5 seconds, previously the minimum was 10 ([`50c55dc`](https://github.com/ryanbdclark/owlet/commit/50c55dcfd30d15027155a8f1d05340238501522d))

## 2023.11.2 (2023-11-23)
### Feature
* Support added for V2 sock ([`50fe1a8`](https://github.com/ryanbdclark/owlet/commit/50fe1a87656b7d6413d06f06f3650fd0bfb48e02))
* Added tests for binary sensors ([`50fe1a8`](https://github.com/ryanbdclark/owlet/commit/50fe1a87656b7d6413d06f06f3650fd0bfb48e02))
### Fix
* Bumping pyowletapi to 2023.11.4 to allow V2 support ([`50fe1a8`](https://github.com/ryanbdclark/owlet/commit/50fe1a87656b7d6413d06f06f3650fd0bfb48e02))
* Refactoring ([`50fe1a8`](https://github.com/ryanbdclark/owlet/commit/50fe1a87656b7d6413d06f06f3650fd0bfb48e02))
* Corrected spelling of sock disconnected sensor ([`50fe1a8`](https://github.com/ryanbdclark/owlet/commit/50fe1a87656b7d6413d06f06f3650fd0bfb48e02))

## 2023.11.1 (2023-11-16)
### Fix
* Bumping pyowletapi to 2023.11.1 ([`3acf847`](https://github.com/ryanbdclark/owlet/commit/3acf8473526665382b44ef6325d708a6c62fff45))
* Sensors and binary sensors are now only created where the sock contains that property, this stops errors where different sock versions have different properties ([`3acf847`](https://github.com/ryanbdclark/owlet/commit/3acf8473526665382b44ef6325d708a6c62fff45))

## 2023.9.1 (2023-09-20)
### Fix
* Bumping pyowletapi to 2023.9.1 to allow for revisions ([`0a7f703`](https://github.com/ryanbdclark/owlet/commit/0a7f70310080a129c988e9607331baa2f6c691e0))
* New revision of sock, revision 5 doesn't report all vitals as before, this would cause the integration to fail to update. Have adjusted the integration to detect the revision and ignore the vitals that are no longer reported ([`0a7f703`](https://github.com/ryanbdclark/owlet/commit/0a7f70310080a129c988e9607331baa2f6c691e0))


## 2023.8.1 (2023-08-21)
### Feature
* 2 new sensors, movement and movement bucket disabled by default, thanks [`@seanford`](https://github.com/seanford) ([`575b213`](https://github.com/ryanbdclark/owlet/commit/575b213ddd732779cd7938e575fc87c8881a69b0))

### Fix
* Various refactoring tasks completed to make this integration more inline with home assistants style guidelines ([`2cd46c1`](https://github.com/ryanbdclark/owlet/commit/c45959b123a6e5f77747475f11d3d3ab67859756))
* Added new sensors to strings jsons ([`2cd46c1`](https://github.com/ryanbdclark/owlet/commit/c45959b123a6e5f77747475f11d3d3ab67859756))

## 2023.7.2 (2023-07-04)
### Fix
* Bumping pyowletapi version to 2023.7.2 ([`c45959b`](https://github.com/ryanbdclark/owlet/commit/c45959b123a6e5f77747475f11d3d3ab67859756))

## 2023.7.1 (2023-07-03)
### Fix
*  Bumping pyowletapi to 2023.7.1 ([`c693fef`](https://github.com/ryanbdclark/owlet/commit/c693fefbf3dba8f35802b87d064401dadbb211b5))
  
## 2023.5.7 (2023-05-30)
### Fix
* Fixed issue with binary sensors not loading, caused by change to way the coordinators are stored ([`8d17317`](https://github.com/ryanbdclark/owlet/commit/8d173174e286b0451cbb2c0d4ae3087028d1ea23))

## 2023.5.6 (2023-05-30)
### Fix
* In light of submitting this as a pull request to the core of HA there have been some refactoring changes to comply with HA's style requirements
* Sensor names now moved to strings file to allow for translations
* Coordinator now properly handles multiple devices
* Spelling of signal strength sensor corrected

### Feature
* Tests added

## 2023.5.5 (2023-05-19)
#### Fix
* Owlet refresh token becomes invalid after 24 hours. Meant that after 1 day the integration would stop working. Moved to pyowletapi v2023.5.28 which uses different refresh token, should no longer need reconfiguring after 24 hours ([`dc58b19`](https://github.com/ryanbdclark/owlet/commit/0141f7d01a9ac9b3e1dcc74cabb896e19bd4a821))

## 2023.5.4 (2023-05-17)
#### Fix
* Bumping to pyowletapi 2023.5.25

## 2023.5.3 (2023-05-17)
#### Fix
* Bumping to pyowletapi 2023.5.24
* Reauthing now no longer re adds users' password to config entry

## 2023.5.2 (2023-05-16)
#### Feature
* Integration now makes use of refresh token from pyowletapi to reauthenticate, user password in no longer stored by integration ([`dc710a1`](https://github.com/ryanbdclark/owlet/commit/dc710a1783a4cad9d6cf355240fe12ac779a87ef))
* New sensors create for baby sleep state ([`9b3392b`](https://github.com/ryanbdclark/owlet/commit/9b3392bdbcd82015ed31d3a50a517e4e22905684))
 
## 2023.5.1 (2023-05-15)
#### Feature
* Changed versioning to date based
### Fix
* Bumping to pyowletapi 2023.5.21 to fix issue with unawaited authentication call, should resolve issue with refreshing authentication ([`228d54b`](https://github.com/ryanbdclark/owlet/commit/228d54b6414e0b9171064254246d1f36c3af8f5b))


## v1.5.0 (2023-05-12)
### Feature
* Now supports reauthentication if credentials have expired/no longer work
* Better error handling when configuring integration, will notify user of incorrect credentials

### Fix
* Removed Owlet specific constants, now using homeassistant generic constants
* On initialisation the integration would crash when trying to update the auth token, the integration would then have to be deleted and setup again
