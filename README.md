# Saving FinishLynx Data

Сервис — асинхронный TCP-сервер (`src/server.py`): принимает построчные
сообщения с результатами полевых видов, парсит их (`src/record.py`) и делает
`replace into` в таблицу `field_lynx` в MySQL. Схема таблицы создаётся при
старте из `src/init.sql`.


## Конфигурация

Все секреты вынесены в файл `.env` (в git **не** коммитится, см. `.gitignore`).
Шаблон с описанием переменных — `.env.example`.

Переменные окружения (читаются в `src/config.py`):

| Переменная | Где задаётся | Формат / значение | Зачем нужна |
|------------|--------------|-------------------|-------------|
| `DB_URL` | `.env` | `mysql+asyncmy://{db_user}:{db_password}@{db_host}:{db_port}/{database_name}` | Подключение к MySQL, куда пишутся результаты (таблица `field_lynx`). Без fallback-значения — обязательна. |
| `PORT` | `.env` | Целое число, по умолчанию `9090` | TCP-порт, который слушает сервер для приёма данных от табло. |

Прочие файлы конфигурации:

| Файл | Назначение |
|------|------------|
| `.env` | Локальные секреты и настройки окружения. **Не в git.** |
| `.env.example` | Шаблон `.env` с описанием переменных (без секретов). В git. |
| `Dockerfile` | Сборка образа Python 3.10, установка зависимостей, запуск `python3 -m src.server`. |
| `Makefile` | Команды `build/run/stop/logs`. `run` поднимает контейнер с `--network host` и `--env-file .env`. |
| `requirements.txt` | Python-зависимости (SQLAlchemy async, asyncmy, loguru). |
| `.dockerignore` / `.gitignore` | Исключают `.env`, `.venv`, `.idea`, кэши из образа и из git. |
| `src/config.py` | Читает `PORT` и `DB_URL` из окружения. |
| `src/init.sql` | Создаёт таблицу `field_lynx`, если её нет (выполняется при старте). |
| `src/migrations/0000.sql` | Разовая миграция схемы (правка первичного ключа). |


## Установка

Подставь реальный `DB_URL`.

```bash
cd ~
git clone https://github.com/shark-andrey/field-lynx-saver.git
cd field-lynx-saver
cp .env.example .env
# отредактируй .env: укажи реальные DB_URL и PORT
nano .env
make build
```

## Запуск

```bash
cd ~/field-lynx-saver && make run
```


## Остановка

```bash
cd ~/field-lynx-saver && make stop
```

## Логи

```bash
cd ~/field-lynx-saver && make logs
```


## Безопасность / секреты

- Секреты хранятся только в `.env`, который в git не коммитится. В репозитории — лишь шаблон `.env.example`.
- Новому окружению: `cp .env.example .env` и подставить реальные значения.
- **Важно:** реквизиты БД ранее уже попадали в публичный репозиторий, поэтому этот пароль нужно считать скомпрометированным и **сменить на стороне БД**. Секрет остаётся в старых коммитах истории — чистка HEAD его оттуда не удаляет.


## Testing (это игнорируй, мне для справки)

```bash
docker run --name mysql -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 -d mysql:latest
mysql --protocol=tcp -hlocalhost -uroot -p
```

```bash
telnet localhost 10000
4,1,1,,13,5,11.08 ,,-0.9 </A SE;4,1,1,,190,4,11.15 ,,-0.9 </A SE;4,1,1,,116,6,12.24 ,,-0.9 </A SE;4,1,1,,297,8,12.29 ,,-0.9 </A SE;4,1,1,,72,2,12.71 ,,-0.9 </A SE;4,1,1,,93,7,13.23 ,,-0.9 </A SE;4,1,1,,171,1,15.42 ,,-0.9 </A SE;4,1,1,,140,3,,,-0.9 </A SE;
```
