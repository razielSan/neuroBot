# 🤖 neuroBot - Telegram bot для генерации изображений,видео и анализа картинок

**neuroBot** - это удобный Telegram-bot который позволяет

- генерировать изображения с помощью разных нейросетей;
- получать описания изображений;
- генерировать короткие видео по изображению;
- использовать несколько внешних API (Caila, Stablehorde, Pollinations)
- отслеживать прогресс выполнения генерации в реальном времени
- безопасно отменять выполнение задач


## 🚀 Запуск проекта

### 1. Установка Python

Убедитесь, что установлен Python **3.8+**

Проверка;

bash

python --version

##  2. Клонирование репозитория

git clone https://github.com/yourname/neurobot.git
cd neurobot


## 3.Создание виртуального окружения

bash

python -m venv venv
source venv/bin/activate      # Linux/MacOS
venv\Scripts\activate         # Windows

## 4.Установка зависимостей 

bash

pip install -r requirements.txt

## 5. Настройка файла .env

Создайте файл .env в папке app/

BOT_TOKEN=ВАШ_ТОКЕН_TELEGRAM
img_desc_models__imagga__ID_IMAGGA_AUTHORIZATION=...
img_gen_models__caila__APIKEY_CAILA_IG=..
img_gen_models__stablehorde__APIKEY_STABLEHORDE_IG=...


## 6. Запуска бота

python app/app.py


## Функциональность

:art: **Генерация изображений**
