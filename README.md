# PTStart_Bot_Tedtoev

# Описание
Это тестовый бот для стажировки PT_Start.

Репозиторий содержит в себе все необходимые файлы и сведения для запуска бота при помощи ansible playbook, кроме файла secrets.yaml.

# Инструкция
#Для успешного запуска программы в ее текущей конфигурации потребуется 3 удаленных хоста. Один - для запуска бота, второй - для запуска БД и третий - для запуска репликатора БД. При желании конфигурация может быть изменена

Пример будет приведен для конфигурации с хостовой kali Linux и тремя удаленными хостами ubuntu server 22.04.

1. На хостовой ОС выполнить следующие команды: apt update; apt apt upgrade; apt-get install git python3-pip; pip3 install ansible; apt install sshpass;
2. Скачать с этого репозитория ветку ansible, можно сделать командой git clone --branch ansible https://github.com/ajamking/PTStart_Bot_Tedtoev.git
3. Перейти в папку скачанного репозитория (будет называться PTStart_Bot_Tedtoev),
4. Создать в ней файл secrets.yaml и инициализировать все переменные своими значениями (его содержимое будет описано ниже),
5. В файле ansible.cfg изменить путь до inventory файла этого проекта (сейчас там строка inventory = /home/kali/Downloads/MY_ANSIBLE/inventory),
6. Убедиться, что на всех удаленных хостах имеется и запущен ssh service,
7. Убедиться, что на всех удаленных хостах пользователь, в качестве которого плейбук будет подключаться к вашим удаленным хостам, имеет достаточно прав. Для тестов можно поступить следующим образом: выполнить команду "sudo visudo" и в самый конец открывшегося файла вписать имя_пользователя ALL=(ALL:ALL) NOPASSWD:ALL
Теперь можно проверить доступность узлов командой ansible all -m ping
8. Запускаем плейбук из директории проекта. Например командой "ansible-playbook playbook_tg_bot.yml -i inventory -e @secrets.yaml"
9. Результатом работы плейбука будет настройка всего необходимого на всех трех удаленных машинах, а также запуск бота в качестве systemd процесса (сервиса), то есть без занятия сессии консоли. Это значит, что и останавливать его нужно будет как сервис.
10. Перейти в телеграм и проверить работоспособность бота отправив ему сообщение.

# Содержание secrets.yaml файла:

```
#Для подключения к машинам - воркерам. Используются в файлике inventory
invent:
  bot:
    host: ???.???.???.???
    user: user_name
    password: user_password
    bot_directory: /srv/Bot_T_A_Ch #Можно оставить так, можно и изменить
  db:
    host: ???.???.???.???
    user: user_name
    password: user_password
  db_repl:
    host: ???.???.???.???
    user: user_name
    password: user_password

#Для подключения к машине-линукс, сведения о которой бот будет собирать бот:
remote_access:
  host: ???.???.???.???
  port: 22 # Если у вас на машине изменен порт по умолчанию, то проставьте его
  user: user_name
  password: user_password
  logfile: Telegram_Bot_Logfile.txt #Можно оставить так, можно и изменить
  tempfile: TempList.txt #Можно оставить так, можно и изменить

#Для подключения к БД
databases:
  master:
    database: db_bot # Можно оставить так, можно и изменить
    port: 5432 # Если у вас на машине изменен порт по умолчанию, то проставьте его
    user: postgres # Желательно оставить так
    password: user_password # Можно оставить так, можно и изменить
  replica:
    port: 5432 # Если у вас на машине изменен порт по умолчанию, то проставьте его
    user: repl_user # Желательно оставить так
    password: user_password # Можно оставить так, можно и изменить

#Токен телеграм бота. Можно получить у botfather.bot 
telegram:
  token: ??????????????????????????????????????
```
