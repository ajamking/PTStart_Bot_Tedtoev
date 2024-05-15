# PTStart_Bot_Tedtoev
Docker images for Telegram bot with PGSQL database for the PT_Start course

# Описание
Это тестовый бот для стажировки PT_Start.

Код разбит на 3 логических раздела - TelegramBot, база данных postgres, а также репликатор базы данных.

Этот репозиторй содержит в себе три образа для создания на их основе docker container-ов.

# Инструкция
#Для успешного запуска программы (трех контейнеров) необходимо (рассмотрим вариант для linux системы):

1. Установить следующие пакеты через apt: git, docker и docker-compose,
2. Скачать с этого репозитория ветку docker,
3. Перейти в папку скачанного репозитория (будет называться PTStart_Bot_Tedtoev),
4. Создать в ней файл .env и инициализировать все переменные своими значениями (его содержимое будет описано ниже),
5. Выполнить команду docker-compose up -d (или модифицировать ее. Цель - поднять все три контейнера),
6. Обратиться к боту через telegram и пользоваться его функционалом.



# Содержание .env файла:
#Все используемые переменные окружения соответствуют шаблонным, а также для удобства была добавлена пара своих:

TOKEN = token - будет содержать токен бота, берется у botfather

RM_HOST = rm_host - будет содержать удаленный хост, который будем мониторить

RM_PORT = rm_port - будет содержать порт удаленного хоста, к которому будем подключаться (рекомендуется 22)

RM_USER = rm_user - будет содержать пользователя удаленного хоста

RM_PASSWORD = rm_password - будет содержать пароль пользователя удаленного хоста

DB_USER = db_user - будет содержать пользователя базы данных удаленного хоста

DB_PASSWORD = db_password - будет содержать пароль пользователя базы данных удаленного хоста

DB_HOST = db_host - будет содержать хост(имя контейнера), в котором будет работать база данных

DB_PORT = db_port - будет содержать порт, на котором работает база данных (рекомендуется 5432)

DB_DATABASE = db_database - будет содержать имя базы данных

DB_REPL_USER = db_repl_user - будет содержать пользователя реплицируемой базы данных (рекомендуется repl_user)

DB_REPL_PASSWORD = db_repl_password - будет содержать пароль пользователя реплицируемой базы данных

DB_REPL_HOST = db_repl_host - будет содержать хост(имя контейнера), в котором будет работать реплицируемая база данных

DB_REPL_PORT = db_repl_port - будет содержать порт, на котором работает реплицируемая база данных (рекомендуется 5432)

PATH_TO_TEMPFILE - путь до временного файла, нужен для удобства работы с найденными ботом данными Называть можно как угодно, например TempList.txt

PATH_TO_LOGFILE - путь до файла с логами. Называть можно как угодно, например Telegram_Bot_Logfile.txt
