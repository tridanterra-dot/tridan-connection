[app]
title = Tridan Connection
package.name = tridan
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,jpeg
version = 1.1
requirements = python3,kivy==2.3.0,cython==0.29.37
orientation = portrait
fullscreen = 0

# Iconos y splash
icon.filename = tridan_logo_icon.png
presplash.filename = tridan_logo_full.png

[buildozer]
log_level = 2
warn_on_root = 0

android.permissions = INTERNET,BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_SCAN,BLUETOOTH_CONNECT,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

p4a.fork = kivy
p4a.branch = develop
