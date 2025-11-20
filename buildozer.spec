[app]
# Имя приложения
title = Calc
# Пакет Python
package.name = calc
package.domain = org.nendie
source.dir = .
source.include_exts = py,png,jpg,kv,txt
version = 0.1
requirements = python3,kivy
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
# Минимальная версия Android
android.minapi = 21
# Версия пакета
android.api = 33
# Версия NDK
android.ndk = 25b
# Разрешения
android.permissions = INTERNET
