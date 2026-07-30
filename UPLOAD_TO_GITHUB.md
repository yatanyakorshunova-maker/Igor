# Быстрая загрузка шаблона на GitHub

1. Распакуйте архив `digital_pet_github_template.zip`.
2. Создайте пустой репозиторий без автоматического README.
3. В репозитории выберите `Add file` → `Upload files`.
4. Перетащите всё содержимое распакованной папки, включая скрытую папку `.github`.
5. Проверьте, что `buildozer.spec` лежит рядом с `main.py`, а workflow находится по пути `.github/workflows/build-apk.yml`.
6. Нажмите `Commit changes`.
7. Откройте `Actions` и дождитесь завершения `Build Android APK`.
8. Скачайте `digital-pet-apk` из блока `Artifacts`.

GitHub не распаковывает загруженный ZIP автоматически, поэтому в репозиторий нужно переносить именно распакованные файлы.
