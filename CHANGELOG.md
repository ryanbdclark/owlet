# Changelog

<!--next-version-placeholder-->

## v1.5.0 (2023-05-12)
### Feature
* Now supports reauthentication if credentials have expired/no longer work
* Better error handling when configuring integration, will notify user of incorrect credentials

### Fix
* Removed Owlet specific constants, now using homeassistant generic constants
* On initialisation the integration would crash when trying to update the auth token, the integration would then have to be deleted and setup again