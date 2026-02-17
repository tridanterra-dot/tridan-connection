[app]

# Título de la app (se muestra en el launcher)
title = Tridan Connection

# Nombre del paquete (debe ser único, en minúsculas, sin espacios)
package.name = tridan

# Dominio del paquete (convención Java-style)
package.domain = org.test

# Directorio con el código fuente
source.dir = .

# Extensiones de archivos a incluir
source.include_exts = py,png,jpg,kv,atlas

# Versión de la app
version = 1.0

# Requisitos: python3 + kivy + pyjnius desde master (fix para 'long' error)
requirements = python3,kivy==2.3.0,https://github.com/kivy/pyjnius/archive/refs/heads/master.zip,cython==0.29.37

# Orientación de la pantalla
orientation = portrait

# No fullscreen por defecto (puedes cambiar a 1 si quieres)
fullscreen = 0

# Permisos Android que necesita tu app
android.permissions = INTERNET,BLUETOOTH,BLUETOOTH_ADMIN,ACCESS_FINE_LOCATION

# Opcional: si usas Bluetooth Low Energy o similar, puedes necesitar más
# android.permissions = INTERNET,BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_CONNECT,BLUETOOTH_SCAN,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION

[buildozer]

# Nivel de log (2 es verbose, útil para debuggear)
log_level = 2

# No adviertas si se ejecuta como root (útil en CI como GitHub Actions)
warn_on_root = 0

# Configuración Android específica
[buildozer:app]

# Bootstrap a usar (sdl2 es el más común para Kivy)
p4a.bootstrap = sdl2

# API Android objetivo (33 es buena para 2024–2026)
android.api = 33

# API mínima soportada
android.minapi = 21

# Versión del NDK (25b es estable y compatible con la mayoría)
android.ndk = 25b

# Arquitecturas a compilar (solo arm64 por ahora para probar más rápido; después puedes volver a ambas)
android.archs = arm64-v8a
# android.archs = arm64-v8a, armeabi-v7a   # descomenta cuando funcione

# Acepta licencia SDK automáticamente
android.accept_sdk_license = True

# No saltes actualizaciones (puedes poner True si quieres acelerar builds repetidos)
android.skip_update = False

# Copia libs extras (útil para algunos casos)
android.copy_libs = 1

# Opcional: si quieres más control sobre python-for-android
# p4a.branch = develop
# p4a.url = https://github.com/kivy/python-for-android.git

# Fin del archivo
