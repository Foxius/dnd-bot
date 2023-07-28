from dotenv import set_key
settings = {
    'token': 'MTEzMjYxNTgyNDIyNjY2MDM1Mg.GOWdMu.a-f4D_qR1QJb7GQ5qFVCDUpR2q7SnNFUjYv4Y8',
    'bot': 'D&D Bot',
    'prefix': '!'
}
# Указываем путь к файлу .env (в этом случае он будет в текущей директории)
dotenv_path = ".env"

# Данные, которые вы хотите сохранить или обновить
name = "John Doe"
email = "johndoe@example.com"

# Записываем данные в файл .env
set_key(dotenv_path, "USER_NAME", name)
set_key(dotenv_path, "USER_EMAIL", email)
