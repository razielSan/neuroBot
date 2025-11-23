# 🤖 NeuroBot - Telegram bot для генерации изображений, видео и анализа картинок

**NeuroBot** - это удобный Telegram-bot который позволяет

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

git clone https://github.com/razielSan/neuroBot.git<br>
cd app


## 3. Создание виртуального окружения

bash

python -m venv venv<br>
source venv/bin/activate      # Linux/MacOS<br>
venv\Scripts\activate         # Windows<br>

## 4. Установка зависимостей 

bash

pip install -r requirements.txt

## 5. Настройка файла .env

Создайте файл .env в папке app/neuroBot/

BOT_TOKEN=ВАШ_ТОКЕН_TELEGRAM<br>
img_desc_models__imagga__ID_IMAGGA_AUTHORIZATION=...<br>
img_gen_models__caila__APIKEY_CAILA_IG=..<br>
img_gen_models__stablehorde__APIKEY_STABLEHORDE_IG=...<br>


## 6. Запуска бота

python app.py


## 🤖 Функциональность

:art: **Генерация изображений**

Поддерживаются сервисы:

* Pollinations
* Caila
* Stablehorde
* Vheer

Вы можете выбрать сервис -> выбрать модель(если есть) -> ввести промпт -><br>
бот отправит вам готовое изображение

:pencil2: **Описание изображений**

Поддерживаются сервисы:

* Imagga

Загрузите картинку - бот проанализирует ее и выдаст описание на русском


:cinema:	**Генерация видео**

Поддерживаются сервисы:

* Vheer

Вводите описание для изображений, загружайте картинку или просто загружайте<br>
изображение и бот на основе полученных данных выдаст вам видео


## :satellite:	**Отслеживание прогресса**

Бот:
- Делает регулярные проверки статуса задач
- Отправляет сообщение о прогрессе, если запрос продолжительный
- Поддерживает отмену, если запрос продолжительный

При нажатии Отмена:
- Останавливается задача
- Бот очищает состояние
- Выполнение завершается корректно

:lock: **Безопасность и стабильность**

Проект содержит:

* Централизованный обработчик ошибок
* безопасные врапперы save_async_execution
* корректную работу с async/await
* фоновые задачи asyncio.create_task()
* контроль таймаутов и зависаний

## 🤖 Структура проекта

app/<br>
 ├── neuroBot/<br>
 │    ├── bot_functions/<br>
 │    ├── configuration/<br>
 │    ├── keyboards/<br>
 │    ├── middleware/<br>
 │    ├── static/<br>
 │    ├── temp/<br>
 │    ├── utils/<br>
 │    ├── views/<br>
 │    ├── main.py<br>
 │    ├── extensions.py<br>
 │    └── .env<br>
 │<br>
 ├── core/ <br>
 ├── logs/ <br>
 ├── settings/ <br>
 ├── erros_handlers/ <br>
 ├── utils/ <br>
 │    <br>
 └── app.py<br>


## :telephone: **Обратная связь**

Если нашли ошибку - создайте Issue или напишите мне в Telegram

[Мой телеграм](https://t.me/razielasus)


## Лицензия

NeuroBot распространяется под лицензией MIT - вы можете использовать его в личных<br>
и коммерческих целях