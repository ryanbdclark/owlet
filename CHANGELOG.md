# Changelog

<!--next-version-placeholder-->
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