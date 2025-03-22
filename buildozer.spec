[app]
title = Juice Vending AI
package.name = juicevendingai
package.domain = org.juicevendingai
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

requirements = python3,kivy,opencv-python-headless,numpy,tensorflow-lite,flask,python-dotenv,pyttsx3,Pillow,mediapipe,scikit-learn,transformers,torch

orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0

android.permissions = CAMERA,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 23b
android.sdk = 31
android.accept_sdk_license = True
android.arch = arm64-v8a

# Thêm các thư viện native
android.enable_androidx = True
android.enable_jetifier = True

[buildozer]
log_level = 2
warn_on_root = 1 