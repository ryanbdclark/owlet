# Changelog

<!--next-version-placeholder-->
## 2023-05-2 (2023-05-16)
#### Feature
* Integration now makes use of refresh token from pyowletapi to reauthenticate, user password in no longer stored by integration ([`dc710a1`](https://github.com/ryanbdclark/owlet/commit/dc710a1783a4cad9d6cf355240fe12ac779a87ef))
* New sensors create for baby sleep state ([`9b3392b`](https://github.com/ryanbdclark/owlet/commit/9b3392bdbcd82015ed31d3a50a517e4e22905684))

## 2023-05-1 (2023-05-15)
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