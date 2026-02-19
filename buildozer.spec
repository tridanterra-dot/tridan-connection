[app]

# Título visible en el launcher
title = Tridan Connection

# Nombre del paquete (único, minúsculas, sin espacios)
package.name = tridan

# Dominio estilo Java
package.domain = org.test

# Directorio fuente
source.dir = .

# Extensiones que se incluyen en el APK
source.include_exts = py,png,jpg,jpeg,kv,atlas

# Versión de la aplicación (cámbiala cuando hagas releases)
version = 1.1

# Requisitos mínimos (cython fijo en 0.29.x para evitar problemas con pyjnius/BLE)
requirements = python3,kivy==2.3.0,cython==0.29.37

# Orientación y fullscreen
orientation = portrait
fullscreen = 0

# Icono (launcher) y presplash (pantalla de carga)
icon.filename = %(source.dir)s/tridan_logo_icon.png
presplash.filename = %(source.dir)s/tridan_logo_full.png

# Permisos necesarios para BLE/mesh offline
# Nota: neverForLocation evita que Android fuerce ubicación precisa
android.permissions = INTERNET,BLUETOOTH,BLUETOOTH_ADMIN,\
                      (name=android.permission.BLUETOOTH_SCAN;usesPermissionFlags=neverForLocation),\
                      BLUETOOTH_CONNECT,\
                      ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION

# Target SDK actualizado (requisito Play Store 2025+)
android.api = 34

# Mínimo SDK razonable para BLE moderno (Android 7+)
android.minapi = 24

# NDK más nuevo y estable (menos problemas con BLE en arm64)
android.ndk = 26c

# Solo arm64-v8a para la prueba (más rápido y suficiente para la mayoría de móviles modernos)
android.archs = arm64-v8a

# Aceptar licencia SDK automáticamente
android.accept_sdk_license = True

# Excluir archivos innecesarios para reducir tamaño y evitar warnings
source.exclude_dirs = tests, .git, .github, __pycache__, *.pyc, build, dist
source.exclude_patterns = *.log, *.bak, *.swp

# Usar fork oficial de Kivy con branch develop (más actualizado para BLE/Kivy 2.3)
p4a.fork = kivy
p4a.branch = develop

[buildozer]

# Nivel de log detallado (útil para debuggear BLE/permisos)
log_level = 2

# No advertir si se ejecuta como root (útil en CI)
warn_on_root = 0

# Opcional: si quieres más control sobre python-for-android
# p4a.url = https://github.com/kivy/python-for-android.git
# Icono de la app (launcher)
icon.filename = %(source.dir)s/tridan_logo_icon.png

# Splash screen (pantalla de carga inicial)
presplash.filename = %(source.dir)s/tridan_logo_full.png

# Tiempo mínimo que se muestra el presplash (en segundos)
# Nota: Android puede ignorarlo si es muy corto, pero 3 segundos suele respetarse
presplash.duration = 3

# Fondo del presplash (opcional, negro por defecto)
presplash.color = #000000
