import telebot
import pickle
from datetime import datetime

# Токен бота
TOKEN = "{{sensitive data}}"

# Создание бота
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения продуктов и их сроков годности
products = {}

# Загрузка словаря из файла, если он существует
try:
    with open('products.pkl', 'rb') as f:
        products = pickle.load(f)
except FileNotFoundError:
    pass

# Обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message):
    """Отправляет сообщение о том, как использовать бота"""
    bot.send_message(message.chat.id, "Привет! Я бот для отслеживания сроков годности продуктов.")
    bot.send_message(message.chat.id, "Команды:")
    bot.send_message(message.chat.id, "- /add - Добавить продукт")
    bot.send_message(message.chat.id, "- /show - Показать список продуктов")
    bot.send_message(message.chat.id, "- /delete - Удалить продукт")

# Обработчик команды /add
@bot.message_handler(commands=["add"])
def add(message):
    """Добавляет продукт в список"""
    args = message.text.split()

    if len(args) != 3:
        bot.send_message(message.chat.id, "Неверный формат команды. Используйте: /add <название продукта> <дата срока годности в формате ДД.ММ.ГГГГ>")
    else:
        product = args[1]
        expiry_date = datetime.strptime(args[2], "%d.%m.%Y")
        today = datetime.now()

        if expiry_date < today:
            products[product] = (expiry_date, "Просрочено")
        else:
            products[product] = (expiry_date, "")

        bot.send_message(message.chat.id, "Продукт добавлен.")

# Обработчик команды /show
@bot.message_handler(commands=["show"])
def show(message):
    """Показывает список продуктов"""
    if not products:
        bot.send_message(message.chat.id, "Список продуктов пуст.")
    else:
        output = "Список продуктов:\n"
        for product, (expiry_date, status) in products.items():
            if status:
                output += f"- {product}: {expiry_date.strftime('%d.%m.%Y')} ({status})\n"
            else:
                output += f"- {product}: {expiry_date.strftime('%d.%m.%Y')}\n"
        bot.send_message(message.chat.id, output)

# Обработчик команды /delete
@bot.message_handler(commands=["delete"])
def delete(message):
    """Удаляет продукт из списка"""
    args = message.text.split()

    if len(args) != 2:
        bot.send_message(message.chat.id, "Неверный формат команды. Используйте: /delete <название продукта>")
    else:
        product = args[1]

        if product in products:
            del products[product]
            bot.send_message(message.chat.id, "Продукт удален.")
        else:
            bot.send_message(message.chat.id, "Продукт не найден.")

# Сохранение словаря в файл при выходе бота
@bot.message_handler(commands=["stop"])
def stop(message):
    """Сохраняет словарь в файл и останавливает бота"""
    with open('products.pkl', 'wb') as f:
        pickle.dump(products, f)
    bot.stop_polling()

# Запуск бота
bot.infinity_polling()
