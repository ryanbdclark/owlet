# Changelog

<!--next-version-placeholder-->
## 2023.08.1 (2023-08-21)
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
  
## 2023.05.7 (2023-05-30)
### Fix
* Fixed issue with binary sensors not loading, caused by change to way the coordinators are stored ([`8d17317`](https://github.com/ryanbdclark/owlet/commit/8d173174e286b0451cbb2c0d4ae3087028d1ea23))

## 2023.05.6 (2023-05-30)
### Fix
* In light of submitting this as a pull request to the core of HA there have been some refactoring changes to comply with HA's style requirements
* Sensor names now moved to strings file to allow for translations
* Coordinator now properly handles multiple devices
* Spelling of signal strength sensor corrected

### Feature
* Tests added

## 2023.05.5 (2023-05-19)
#### Fix
* Owlet refresh token becomes invalid after 24 hours. Meant that after 1 day the integration would stop working. Moved to pyowletapi v2023.5.28 which uses different refresh token, should no longer need reconfiguring after 24 hours ([`dc58b19`](https://github.com/ryanbdclark/owlet/commit/0141f7d01a9ac9b3e1dcc74cabb896e19bd4a821))

## 2023.05.4 (2023-05-17)
#### Fix
* Bumping to pyowletapi 2023.5.25

## 2023.05.3 (2023-05-17)
#### Fix
* Bumping to pyowletapi 2023.5.24
* Reauthing now no longer re adds users' password to config entry

## 2023.05.2 (2023-05-16)
#### Feature
* Integration now makes use of refresh token from pyowletapi to reauthenticate, user password in no longer stored by integration ([`dc710a1`](https://github.com/ryanbdclark/owlet/commit/dc710a1783a4cad9d6cf355240fe12ac779a87ef))
* New sensors create for baby sleep state ([`9b3392b`](https://github.com/ryanbdclark/owlet/commit/9b3392bdbcd82015ed31d3a50a517e4e22905684))
 
## 2023.05.1 (2023-05-15)
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
