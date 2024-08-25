# DND_Bot

Бот для РРИ, в будущем для нескольких РРИ

## Обзор

DnD_Bot - это помощник для командных игр. В него можно играть рабочим коллективом или семьей. Он может помочь сыграть в ДнД без специального оборудования. Он улучшает оригинальную версию, добавляя в неё изображения и аудио.

## Структура

```structure
DND_Bot/
├── bot_commands/
|   ├── DNS_commands
|   |   ├── __init__.py
|   |   ├── Character.py
|   |   ├── create_character.py
|   |   └── roll_dices.py
│   ├── __init__.py
│   ├── MultiPLayer.py
│   └── support.py
├── classes/
|   ├── DND_Staff.py
|   |   ├── __init__.py
|   |   ├── ClassResource.py
|   |   ├── RaceResource.py
|   |   └── dyces.py
│   ├── __init__.py
│   ├── DnD_Player.py
│   └── Room.py
├── DataBase/
│   ├── __init__.py
│   ├── manager.py
│   └── users.json
├── GenerModels/
│   ├── __init__.py
│   ├── API_T2I.py
│   └── GigaChat.py
├── srcs/
│   ├── dnd/
│   └── imgs/
├── utils
│   ├── __init__.py
│   └── teleWidgets.py
├── .env
├── .gitignore
├── LICENSE
├── main.py
└── README.md
```

## Инструкция

### 1. Установите питон:
...

## Используемые технологии

- **Модели**: Использование моделей GigaChat, Kandinsky, | Dall-E 3 |

- **Telegram Bot API**: Использование Aiogram