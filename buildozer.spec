[app]
title = Tridan Connection
package.name = tridan
package.domain = org.test
source.dir = .
source.include_exts = py
version = 1.0
requirements = python3,kivy,pyjnius
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 0

android.permissions = INTERNET,BLUETOOTH,BLUETOOTH_ADMIN,ACCESS_FINE_LOCATION
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
android.skip_update = False
android.copy_libs = 1
