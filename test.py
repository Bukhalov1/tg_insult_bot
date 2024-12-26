#! /usr/bin/python
import time
import random
import csv
from aiogram import Bot, types, dispatcher, executor
import config
# from list_of_insults import list_of_insults

bot = Bot(token=config.TOKEN)
dp = dispatcher.Dispatcher(bot)

# Путь к CSV файлу
file_path = 'list_of_groups.csv'
# Читаем данные из CSV файла и сохраняем их в переменной
with open(file_path, mode='r') as file:
    reader = csv.reader(file)
    data = list(reader)

my_group_id = 397033764 #-4044391196 # моя
# group_id = "-1001667799944" # триумвират
# group_id = "-1001974589265" # киты 
# group_id = "" #лрз

last_insults = []

with open("list_of_insults.csv", mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    list_of_insults = next(reader)        

def check_group(n):
    # Проверяем, есть ли число в данных
    number_found = False 
    for row in data:
        if str(n) in row:
            number_found = True
            break
    # Если число не найдено, добавляем его в переменную и в файл
    if not number_found:
        data.append([n])
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

def rand_func():
    l = len(list_of_insults) - 1
    random.seed(time.time())
    rand1 = random.randint(0, l)
    rand2 = random.randint(0, l)
    combined_rand = (rand1 + rand2) % l 
    return combined_rand

def choose_an_insult(last_insults):
    i = 0
    if abs(len(last_insults) - len(list_of_insults)) > 20:
        last_insults = []
    while 1:
        i = i + 1
        choosen_insult = list_of_insults[rand_func()]
        if choosen_insult not in last_insults or i > 5:
            break
    last_insults.append(choosen_insult)
    return choosen_insult


async def on_startup(_):
    print("TG bot is online")

@dp.message_handler()
async def masg_analisys(message: types.Message):
    print(message.chat.id, message.text)
    
    message_id = message.message_id
    group_id = message.chat.id
    message_text = message.text.lower()
    check_group(group_id)
    # await bot.send_message(message.from_user.id, message.chat.id) # id of chat
    if "оскорби его" in message_text:
        cur_insult = choose_an_insult(last_insults)
        await bot.send_message(group_id, f"Ну ты {cur_insult}", reply_to_message_id = message_id-1)

    if "оскорбить" in message_text and "раз" in message_text:
        name = ''
        tex = ''
        msg = message_text.split() #message.text.split()
        for i in msg:
            if i != "оскорбить":
                name = name + " " + i 
            else:
                break
        times = int(msg[-2])
        if times >= 6:
            times = 5
            tex = "В бесплатном тарифе вы не можете оскорблять более пяти раз.\n\rЧтобы оскоблять неограниченное количество раз, оплатите подписку за 1 TON/мес по адресу UQASJD_wNvEzj5sV_R5a9A8DGpS-mOPTvhFGPDl5cBd3Y6M3\n\r" 
            await bot.send_message(group_id, f"{tex}\n\r")
        # await bot.send_message(group_id, f"{tex}\n\rЗапускаю оскорбления пользователя {name} {times} {msg[-1]}")
        for i in range(times):
            cur_insult = choose_an_insult(last_insults)
            await bot.send_message(group_id, f"{name} {cur_insult}")
            rand_time = round(random.uniform(0.1, 1.5), 1)
            time.sleep(rand_time)
    if "оскорби себя" in message_text:
        # await bot.send_message(group_id, "Запускаю оскорбления")
        cur_insult = choose_an_insult(last_insults)
        await bot.send_message(group_id, f"Я бот-оскорбитель этого чата [{group_id}], и я еще тот {cur_insult}")

    if "анекдот дня" in message_text and group_id == my_group_id:
        for i_group in data:
            i_group = int(i_group[0])
            cur_insult = choose_an_insult(last_insults)
            await bot.send_message(i_group, f"Ты - {cur_insult}, если не посмеёшься над анедотом дня! Кстати вот он.\n\r{message.text}")

    if "добавить оскорбление" in message_text:
        input_str = message.text
        message_id = message.message_id
        an_insult = input_str.replace("добавить оскорбление ", "")
        list_of_insults.append(an_insult)
        with open("list_of_insults.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(list_of_insults)
        await bot.send_message(group_id, f"Спасибо, {an_insult}, я пополнил свой словарный запас", reply_to_message_id=message_id)

    if "ты пидор" in message_text or "ты пидр" in message_text or "ты пидорас" in message_text:
        cur_insult = choose_an_insult(last_insults)
        await bot.send_message(group_id, f"А ты тогда {cur_insult}!",  reply_to_message_id=message_id)
        
    if "да" in message_text[-3:]:
        yes_list = ["Перда", "Пизда", "Манда", "Елда"]
        r = random.randint(0, len(yes_list)-1)
        await bot.send_message(group_id, f"{yes_list[r]}!",  reply_to_message_id=message_id)

if __name__ == "__main__":
    last_insults = []
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
