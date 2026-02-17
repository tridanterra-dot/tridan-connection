[app]
title = Tridan Connection
package.name = tridan
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# <<<=== ESTA ES LA LÍNEA CLAVE ===>>>
requirements = python3,kivy==2.3.0,https://github.com/kivy/pyjnius/archive/refs/heads/master.zip,cython==0.29.37

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,BLUETOOTH,BLUETOOTH_ADMIN,ACCESS_FINE_LOCATION

[buildozer]
log_level = 2
warn_on_root = 0

# Extra para forzar versión moderna de python-for-android (ayuda mucho)
p4a.branch = develop

# Configuración Android
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a          # solo una arquitectura para que sea más rápido esta vez
android.accept_sdk_license = True
android.skip_update = False
android.copy_libs = 1
