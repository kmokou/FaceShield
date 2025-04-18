# FaceShield - защита персональных данных

## Описание
FaceShield - это программа для автоматического скрытия экрана при обнаружении посторонних лиц. Использует веб-камеру для распознавания лиц и мгновенно активирует защиту, когда за компьютером находится неавторизованный пользователь.
  
## Требования
### Минимальные:
- ОС: Windows 10/11, Linux (Ubuntu 20.04+, Debian 11+)
- Процессор: Intel Core i5 / AMD Ryzen 3
- Оперативная память: 4 ГБ ОЗУ
- Камера: Встроенная или внешняя веб-камера (минимум 720p)
### Рекомендуемые:
- ОС: Windows 11, Linux (Ubuntu 22.04+, Arch)
- Процессор: Intel Core i7 / AMD Ryzen 5 и выше
- Оперативная память: 8 ГБ ОЗУ и выше
- Камера: Внешняя веб-камера 1080p+ с автофокусом
- Дополнительные требования: GPU с поддержкой CUDA (для более быстрой работы)


## Установка на Windows
1. Скачайте архив с программой
2. Распакуйте в отдельную папку
3. Запустите `install.bat` (требуются права администратора)
4. Примите условия политики конфиденциальности
5. Дождитесь завершения установки зависимостей

## 🐧 Установка на Linux

```bash
# Клонируйте репозиторий
git clone https://github.com/kmokou/FaceShield.git
cd FaceShield

# Установите зависимости
pip install -r requirements.txt

# Запустите GUI
python gui.py
```

## Первый запуск
1. Запустите `run_face_shield.bat` на Windows или `gui.py` на Linux
2. Нажмите кнопку "REGISTER" для регистрации своего лица
3. Расположите лицо перед камерой и нажмите "С" для захвата изображения
4. Нажмите "START" для запуска защиты

## Использование
- Программа автоматически скроет экран при отсутствии авторизованного пользователя
- Для выхода нажмите Q или кнопку ВЫХОД в интерфейсе

## Безопасность
Все данные обрабатываются локально, изображения не сохраняются и не передаются.
