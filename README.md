### Hexlet tests and linter status:
[![Actions Status](https://github.com/AlloKuz/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/AlloKuz/python-project-52/actions)
[![build](https://github.com/AlloKuz/python-project-52/actions/workflows/build.yml/badge.svg)](https://github.com/AlloKuz/python-project-52/actions/workflows/build.yml)

# Менеджер задач

## *Учебный проект: управление задачами с возможностью регистрации пользователей*

## Описание

Основная задача приложения -- позволить нескольким пользователями управлять задачами.
Приложение даёт возможность зарегистрированным пользователям создавать, изменять и удалять задачи,
а также связанные с ними элементы. Приложение поддерживает ведение статусов задач и создание меток.

## Установка и запуск

Для запуска приложение необходимо настроить параметры приложения в файл `.env`, либо в переменные окружения.

Установка приложения начинается с установки `poetry` и запуска скрипта `build.sh`:

```bash
pip install poetry

./build.sh
```

Далее запуск приложения управляется файлом Makefile. 
Для запуска отладочной версии используйте `make dev`.

## Пример работы:

https://python-project-52-lmoi.onrender.com

![Screenshot 1](.github/images/users.jpg)

![Screenshot 1](.github/images/tasks.jpg)

![Screenshot 1](.github/images/create.jpg)

![Screenshot 1](.github/images/tasks2.jpg)