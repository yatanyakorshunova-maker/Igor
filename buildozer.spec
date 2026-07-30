[app]

title = Мой цифровой питомец
package.name = digitalpet
package.domain = org.creativika

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt
source.exclude_dirs = tests,docs,.github,__pycache__,.venv,.git

version = 1.0.0
requirements = python3==3.13.7,hostpython3==3.13.7,kivy==2.3.1

icon.filename = assets/icon.png
presplash.filename = assets/presplash.png
orientation = portrait
fullscreen = 0

# Параметры Android. API 24 нужен для preadv/pwritev, используемых современным CPython.
android.api = 36
android.minapi = 24
android.ndk = 29
android.archs = arm64-v8a
android.private_storage = True
android.enable_androidx = True
android.accept_sdk_license = True

# Зафиксированная версия python-for-android. Python 3.13 указан отдельно в requirements.
p4a.branch = v2026.05.09

[buildozer]
log_level = 2
warn_on_root = 1
