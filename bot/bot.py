import logging, re, os, paramiko, re, psycopg2

from dotenv import main
from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)

# Подключение переменных из окружения
main.load_dotenv()
TOKEN = os.getenv('TOKEN')

PATH_TO_LOGFILE = os.getenv('PATH_TO_LOGFILE')
PATH_TO_TEMPFILE = os.getenv('PATH_TO_TEMPFILE')

RM_HOST = os.getenv('RM_HOST')
RM_PORT = os.getenv('RM_PORT')
RM_USER = os.getenv('RM_USER')
RM_PASSWORD = os.getenv('RM_PASSWORD')

DB_DATABASE = os.getenv('DB_DATABASE')

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

#Пока непонятно зачем они тут нужны
DB_REPL_HOST = os.getenv('DB_REPL_HOST')
DB_REPL_PORT = os.getenv('DB_REPL_PORT')
DB_REPL_USER = os.getenv('DB_REPL_USER')
DB_REPL_PASSWORD = os.getenv('DB_REPL_PASSWORD')

# Подключение логирования
logging.basicConfig(
    filename=PATH_TO_LOGFILE, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Базовые функции
def StartCommand(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')

def HelpCommand(update: Update, context):
    update.message.reply_text('Help!')

def ReturnEcho(update: Update, context):
    update.message.reply_text(update.message.text)

# Диалоги
def FindPhoneNumbers (update: Update, context):
    user_input = update.message.text # Получаем текст, содержащий(или нет) номера телефонов

    if user_input == 'да':
        connection = psycopg2.connect( host=DB_HOST, port=DB_PORT, database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD )
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM phones;")
            data = cursor.fetchall()

            file = open(PATH_TO_TEMPFILE, 'r')
            phoneNumbers = file.readlines()
            file.close()         
            
            counter = 1
            for phone in phoneNumbers:
                phone = phone[:-1]
                new_id = len(data) + counter
                command = f"INSERT INTO phones (phoneID, phone) VALUES ({new_id}, '{phone}');"
                counter = counter + 1
                cursor.execute(command)

            connection.commit()
            logging.info("Команда INSERT успешно выполнена")
            update.message.reply_text('Команда INSERT успешно выполнена')
        except Exception as ex :
            logging.error(f"Команда INSERT закончилась с ошибкой: {ex.with_traceback}")
            update.message.reply_text(f'Команда INSERT закончилась с ошибкой: {ex.with_traceback}')
        finally:
            connection.commit()
            return ConversationHandler.END

    if user_input == 'нет':
        update.message.reply_text('Ну и не надо')
        return ConversationHandler.END

    phoneNumRegex = re.compile(r'(?:\+7|8)(?: \(\d{3}\) \d{3}-\d{2}-\d{2}|\d{10}|\(\d{3}\)\d{7}| \d{3} \d{3} \d{2} \d{2}| \(\d{3}\) \d{3} \d{2} \d{2}|-\d{3}-\d{3}-\d{2}-\d{2})')

    phoneNumberList = phoneNumRegex.findall(user_input) # Ищем номера телефонов

    if not phoneNumberList: # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Телефонные номера не найдены')
        return ConversationHandler.END
    
    with open(PATH_TO_TEMPFILE, 'w+') as file:
        for items in phoneNumberList:
            file.write('%s\n' %items)
        file.close()

    phoneNumbers = '' # Создаем строку, в которую будем записывать номера телефонов
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i+1}. {phoneNumberList[i]}\n' # Записываем очередной номер
    update.message.reply_text('Найдены следующие телефонные номера:')
    update.message.reply_text(phoneNumbers)
    update.message.reply_text('Хотите сохранить их в базу? Введите да или нет')
def FindPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')
    return 'find_phone_number'

def FindEmailAddresses (update: Update, context):
    user_input = update.message.text

    if user_input == 'да':
        connection = psycopg2.connect( host=DB_HOST, port=DB_PORT, database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD )

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM emails;")
            data = cursor.fetchall()

            file = open(PATH_TO_TEMPFILE, 'r')
            emails = file.readlines()
            file.close()         
            
            counter = 1
            for email in emails:
                email = email[:-1]
                new_id = len(data) + counter
                command = f"INSERT INTO emails (emailID, email) VALUES ({new_id}, '{email}');"
                counter = counter + 1
                cursor.execute(command)

            connection.commit()
            logging.info("Команда INSERT успешно выполнена")
            update.message.reply_text('Команда INSERT успешно выполнена')
        except Exception as ex :
            logging.error(f"Команда INSERT закончилась с ошибкой: {ex.with_traceback}")
            update.message.reply_text(f'Команда INSERT закончилась с ошибкой: {ex.with_traceback}')
        finally:
            connection.commit()
            return ConversationHandler.END

    if user_input == 'нет':
        update.message.reply_text('Ну и не надо')
        return ConversationHandler.END
    
    emailRegex = re.compile(r'[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)')
    emailAddressesList = emailRegex.findall(user_input)

    if not emailAddressesList:
        update.message.reply_text('Адреса электронных почт не найдены')
        return ConversationHandler.END
    
    with open(PATH_TO_TEMPFILE, 'w+') as file:
        for items in emailAddressesList:
            file.write('%s\n' %items)
        file.close()

    emails = '' 
    for i in range(len(emailAddressesList)):
        emails += f'{i+1}. {emailAddressesList[i]}\n' 
    update.message.reply_text('Найдены следующие электронные адреса:')
    update.message.reply_text(emails)
    update.message.reply_text('Хотите сохранить их в базу? Введите да или нет')
def FindEmailAddressesCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска Email-адресов: ')
    return 'find_email'

def VerifyPasswordSafety (update: Update, context):
    user_input = update.message.text 

    passwordRegex = re.compile('^.*(?=.{8,})(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!#$%&? "]).*$')

    passwordRegex = passwordRegex.fullmatch(user_input)

    if not passwordRegex:
        update.message.reply_text('Пароль слишком простой')
        return ConversationHandler.END
    else:
        update.message.reply_text('Пароль сложный, подходит')
        return ConversationHandler.END
def VerifyPasswordSafetyCommand(update: Update, context):
    update.message.reply_text('Введите пароль для проверки его надежности: ')
    return 'verify_password'

# Команды бота для Linux-мониторинга
def GetReleaseCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect( hostname= RM_HOST, port = RM_PORT, username = RM_USER, password = RM_PASSWORD )
    
    stdin, stdout, stderr = client.exec_command('cat /etc/*-release')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def GetUnameCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect( hostname= RM_HOST, port = RM_PORT, username = RM_USER, password = RM_PASSWORD )

    stdin, stdout, stderr = client.exec_command('hostnamectl')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def GetUptimeCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect( hostname= RM_HOST, port = RM_PORT, username = RM_USER, password = RM_PASSWORD )
    stdin, stdout, stderr = client.exec_command('uptime')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def GetDFCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect( hostname= RM_HOST, port = RM_PORT, username = RM_USER, password = RM_PASSWORD )

    stdin, stdout, stderr = client.exec_command('df')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def GetFreeCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect( hostname= RM_HOST, port = RM_PORT, username = RM_USER, password = RM_PASSWORD )
    
    stdin, stdout, stderr = client.exec_command('free -m')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def GetMpStatCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect( hostname= RM_HOST, port = RM_PORT, username = RM_USER, password = RM_PASSWORD )
    
    stdin, stdout, stderr = client.exec_command('free -m')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def GetWCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect( hostname= RM_HOST, port = RM_PORT, username = RM_USER, password = RM_PASSWORD )
    
    stdin, stdout, stderr = client.exec_command('w')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def GetWCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect( hostname= RM_HOST, port = RM_PORT, username = RM_USER, password = RM_PASSWORD )
    
    stdin, stdout, stderr = client.exec_command('w')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def GetAuthsCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect( hostname= RM_HOST, port = RM_PORT, username = RM_USER, password = RM_PASSWORD )
    
    stdin, stdout, stderr = client.exec_command('last -n 10')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def GetCriticalCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect( hostname= RM_HOST, port = RM_PORT, username = RM_USER, password = RM_PASSWORD )
    
    stdin, stdout, stderr = client.exec_command('journalctl -p 2 -n 5')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def GetPSCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect( hostname= RM_HOST, port = RM_PORT, username = RM_USER, password = RM_PASSWORD )
    
    stdin, stdout, stderr = client.exec_command('ps')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def GetSSCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect( hostname= RM_HOST, port = RM_PORT, username = RM_USER, password = RM_PASSWORD )
    
    stdin, stdout, stderr = client.exec_command('netstat -tulpn')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def GetAptList(update: Update, context):
    user_input = update.message.text 
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect( hostname= RM_HOST, port = RM_PORT, username = RM_USER, password = RM_PASSWORD )

    if user_input == 'all':
        stdin, stdout, stderr = client.exec_command('dpkg -l | head -n 25')
        data = stdout.read() + stderr.read()
        client.close()
        data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
        update.message.reply_text(data)
        return ConversationHandler.END 
    else:
        stdin, stdout, stderr = client.exec_command('apt show '+user_input)
        data = stdout.read() + stderr.read()
        client.close()
        data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
        update.message.reply_text(data)
        return ConversationHandler.END
def GetAptListCommand(update: Update, context):
    update.message.reply_text('Введите all чтобы посмотреть все пакеты или название конкретного')
    return 'get_apt_list'

def GetServicesCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect( hostname= RM_HOST, port = RM_PORT, username = RM_USER, password = RM_PASSWORD )
    
    stdin, stdout, stderr = client.exec_command('systemctl list-units --type=service | head -n 25')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def GetReplLogsCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    update.message.reply_text(DB_HOST)
    update.message.reply_text(RM_PORT)
    update.message.reply_text(DB_USER)
    update.message.reply_text(DB_PASSWORD)
    client.connect( hostname = DB_HOST, port = RM_PORT, username = DB_USER, password = DB_PASSWORD )
    
    stdin, stdout, stderr = client.exec_command('cat grep repl_user /var/log/postgresql/postgresql.log | tail -n 10')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def GetEmailsCommand(update: Update, context):
    connection = psycopg2.connect( host=DB_HOST, port=DB_PORT, database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD )
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM emails;")
    data = cursor.fetchall()
    logging.info("Команда SELECT успешно выполнена")
   
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def GetPhoneNumbersCommand(update: Update, context):
    connection = psycopg2.connect( host=DB_HOST, port=DB_PORT, database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD )
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM phones;")
    data = cursor.fetchall()
    logging.info("Команда SELECT успешно выполнена")
    for row in data:
        print(row)
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    
    update.message.reply_text(data)

def main():
    updater = Updater(TOKEN, use_context=True)
    
    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher
  
    #Диалоги для обработчиков
    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', FindPhoneNumbersCommand)],
        states={'find_phone_number': [MessageHandler(Filters.text & ~Filters.command, FindPhoneNumbers)]}, 
        fallbacks=[]
    )
    
    convHandlerFindEmails = ConversationHandler(
        entry_points=[CommandHandler('find_email', FindEmailAddressesCommand)],
        states={'find_email': [MessageHandler(Filters.text & ~Filters.command, FindEmailAddresses)]}, 
        fallbacks=[]
    )

    convHandlerVerifyPassword = ConversationHandler(
        entry_points=[CommandHandler('verify_password', VerifyPasswordSafetyCommand)],
        states={'verify_password': [MessageHandler(Filters.text & ~Filters.command, VerifyPasswordSafety)]}, 
        fallbacks=[]
    )
 
    convHandlerGetTheApt = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', GetAptListCommand)],
        states={'get_apt_list': [MessageHandler(Filters.text & ~Filters.command, GetAptList)]}, 
        fallbacks=[]
    )

    # Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", StartCommand))
    dp.add_handler(CommandHandler("help", HelpCommand))
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmails)
    dp.add_handler(convHandlerVerifyPassword)
    dp.add_handler(CommandHandler("get_release", GetReleaseCommand))
    dp.add_handler(CommandHandler("get_uname", GetUnameCommand))
    dp.add_handler(CommandHandler("get_uptime", GetUptimeCommand))
    dp.add_handler(CommandHandler("get_df", GetUptimeCommand))
    dp.add_handler(CommandHandler("get_free", GetFreeCommand))
    dp.add_handler(CommandHandler("get_mpstat", GetMpStatCommand))
    dp.add_handler(CommandHandler("get_w", GetWCommand))
    dp.add_handler(CommandHandler("get_auths", GetAuthsCommand))
    dp.add_handler(CommandHandler("get_critical", GetCriticalCommand))
    dp.add_handler(CommandHandler("get_ps", GetPSCommand))
    dp.add_handler(CommandHandler("get_ss", GetSSCommand))
    dp.add_handler(convHandlerGetTheApt)
    dp.add_handler(CommandHandler("get_services", GetServicesCommand))
    dp.add_handler(CommandHandler("get_repl_logs", GetReplLogsCommand))
    dp.add_handler(CommandHandler("get_emails", GetEmailsCommand))
    dp.add_handler(CommandHandler("get_phone_numbers", GetPhoneNumbersCommand))
    
    # Базовый обработчик для текстовых сообщений.
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, ReturnEcho))
    
    # Запускаем бота
    updater.start_polling()
	# Останавливаем бота при нажатии Ctrl+C
    updater.idle()

if __name__ == '__main__':
    main()
