[app]
title = Tridan Connection
package.name = tridan
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Excluir carpetas problemáticas de pyjnius (evita SyntaxError en compileall por código Python 2)
source.exclude_dirs = patched_pyjnius/tests, patched_pyjnius/docs, patched_pyjnius/examples, patched_pyjnius/.git

# Excluir patrones comunes (mejora limpieza general)
source.exclude_patterns = *.pyc, __pycache__*, .git*, .github*, *.log, tests*, examples*, docs*

requirements = python3,kivy==2.3.0,https://github.com/kivy/pyjnius/archive/refs/heads/master.zip,cython==0.29.37

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,BLUETOOTH,BLUETOOTH_ADMIN,ACCESS_FINE_LOCATION

[buildozer]
log_level = 2
warn_on_root = 0

# Forzar branch develop de p4a (más actualizado y con fixes recientes)
p4a.branch = develop

# Configuración Android
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a          # solo una para prueba rápida (después puedes poner arm64-v8a,armeabi-v7a)
android.accept_sdk_license = True
android.skip_update = False
android.copy_libs = 1


