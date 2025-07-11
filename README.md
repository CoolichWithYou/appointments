# Appointment project

## Содержание

1. [Описание](#1-описание)
2. [Эндпоинты](#3-Эндпоинты)
3. [Переменные среды](#3-переменные-среды)
4. [Диаграммы](#4-диаграммы)
5. [Проектирование-реализация](#5-проектирование-реализация)
6. [Telegram-bot](#6-telegram---bot-с-ии-подбором-врача)

## 1. Описание

Минимальный, но полноценный микросервис для записи пациентов. Для запуска compose сборки локально
нужно прописать

`docker compose up --build`

Переменные среды из `.env.example` автоматически подтянутся и будут использоваться как `db`,
так и `fastapi` сервером в контейнерах.

`fastapi` не запустится пока `db` не будет инициализирована полностью. За это отвечает `wait-for-db.sh`.
Т.к. `depends on` в compose файле гарантирует только ожидание запуска контейнера, а не его готовность
принимать подключения.

### Важно!
Чтобы проект прошёл все `ci` проверки, надо выставить [секреты репозитория](https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-guides/using-secrets-in-github-actions) в github actions

## 2. Эндпоинты

- `POST /appointments` - создать запись;
- `GET /appointments/{id}` - получить запись по ID;

## 3. Переменные среды

|  Переменная среды | Значение по умолчанию | Краткое описание      |
|------------------:|:----------------------|-----------------------|
|           DB_HOST | db                    | адрес контейнера с бд |
|           DB_PORT | 5432                  | порт базы данных      |
|       POSTGRES_DB | dbname                | название базы данных  |
|     POSTGRES_USER | username              | пользователь бд       |
| POSTGRES_PASSWORD | password              | пароль бд             |

## 4. Диаграммы

Архитектурная схема `/diagrams/architecture.png`  
ER-диаграмма `/diagrams/er.png`  
Activity-диаграмма `/diagrams/activity.png`  
[Документ бизнесс-процесса](https://miro.com/welcomeonboard/K2UvTFh4ZFNoYU10SERnbTJQNjJqb01IL1VNaTdLVFBvbmZxNm9rNU5sanRwR1BQeXlBRmI4YkFkNmU0NGVaTjNSeTdTdkpuZkZmNDB1MVllWGw2Yndub2NidW1pNFhoSWR4N3RaQTc0WW1NREQ2cDZLWHMrUW5Yd2VQdFVJY1FnbHpza3F6REdEcmNpNEFOMmJXWXBBPT0hdjE=?share_link_id=575849172273)

## 5. Проектирование-реализация

|               Название шага | Реализация                                     |
|----------------------------:|:-----------------------------------------------|
|  Проектирование архитектуры | Выбор микросервисной архитектуры               |
|          Проектирование API | Единый формат ошибок, RESTful стандарт         |
|           Проектирование БД | ER-диаграмма, нормализация схемы               |
|                  Реализация | compose.yml с сервисами бд и fastapi, makefile |
| Валидация проектных решений | Написание тестов                               |

## 6. Telegram - bot с ИИ-подбором врача

1. Бот спрашивает ФИО, затем номер телефона.
2. Бот предлагает 2 варианта - выбор врача, либо описать симптомы.
3. Если выбран первый вариант - бот загружает свободные даты и время приёма с пагинацией в markup
4. Если пользователь решил описать симптомы, LLM определяет специализацию и запрашивает данные из бд

В качестве ML библиотеки решил использовать `scikit-learn` с собственным датасетом. Пример находится в /model. 
В symptoms.csv находится пара "описание симптома" -> "нужный врач". 
Чтобы натренировать модель `python train`, чтобы предсказать `python predict`
