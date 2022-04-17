from aiogram import types, Dispatcher
from create_bot import bot, dp
from keyboards import inl_kb, kb_menu
from datetime import datetime
from  data_base import cur, base

    # СТАРТ
@dp.message_handler(commands=['start', 'Меню'])
async def start_command(message : types.Message):
    await bot.send_message(message.from_user.id, "Этот бот помогает вам отслеживать ваши траты.\n\nКак записывать расходы\nВведите:\nкатегорию сумму\n\nПример:  транспорт  150", reply_markup= kb_menu)
    await message.delete()

    # РАСХОДЫ ЗА МЕСЯЦ
@dp.message_handler(text= 'Расходы за месяц')    
async def mounth_update(message : types.Message):
    now = datetime.now()
    format_data = ''
    all_data = cur.execute('SELECT * FROM spendings').fetchall() 
    for info in all_data:
        if info[2] == now.strftime('%m'):
            for element in info[:-1]:
                format_data += str(element) + "  "
            format_data += '\n'
    await bot.send_message(message.from_user.id, f'Ваши расходы за  месяц:\n{format_data}')
    await message.delete() 

    # ПОДТВЕРЖЕНИЕ ЧЕРЕЗ ИНЛАЙН КНОПУ
@dp.message_handler(text='Удалить данные')
async def delete_confirmation(message : types.Message):
    await bot.send_message(message.from_user.id, 'Вы действительно хотите удалить все данные?', reply_markup= inl_kb)
   
   # УДАЛЕНИЕ
@dp.callback_query_handler(text='delete_all_data')
async def delete_expenses(callback : types.CallbackQuery):
    cur.execute('DELETE FROM spendings')   
    await callback.answer('База данных успешно удалена')

    # РАСХОДЫ  
@dp.message_handler(text= 'Показать расходы')
async def show_expenses(message : types.Message):
    all_data = cur.execute('SELECT category, count FROM spendings').fetchall()
    format_data = ' '
    all_time_data = {}
    for info in all_data:
        if info[0] in all_time_data:
            all_time_data[info[0]] += info[1]
        else:
            all_time_data.update({info[0]: info[1]})
    # ФОРМАТИРУЕМ КОРТЕЖ
    for new_data in all_time_data.items():
        for element in new_data:
            format_data += str(element) + "  "
        format_data += '\n'
    await bot.send_message(message.from_user.id, f'Ваши расходы:\n{format_data}')
    await message.delete()

    # ВВОД В БАЗУ 
@dp.message_handler()
async def add_expense(message : types.Message):
    now = datetime.now()
    split_message = message.text.split()
    all_category = cur.execute('SELECT category FROM spendings').fetchall()
    date = cur.execute('SELECT date FROM spendings').fetchall()
    try:
        if type(split_message[0]) ==  str and type(int(split_message[1])) == int:
            entered_category = (split_message[0].capitalize(),)
            if entered_category in all_category and (now.strftime('%m'),) in date:
                category_count, = cur.execute('SELECT count FROM spendings WHERE category == ?', (*entered_category,)).fetchone() 
                print(category_count)
                # ПОДТВЕРЖДЕНИЕ С ПОМОЩЬЮ ИНЛАЙН КНОПОК
                cur.execute('UPDATE spendings SET count == ? WHERE category == ?',(int(category_count) + int(split_message[1]), *entered_category))
                base.commit()
            else:
                cur.execute('INSERT INTO spendings VALUES(?, ?, ?)', (*entered_category, int(split_message[1]), now.strftime('%m')))
                base.commit()
                print(date, tuple(now.strftime('%m')))
        else:
            await bot.send_message(message.from_user.id, 'Введите:\nкатегорию сумму\n\nПример:  транспорт  150')
    except ValueError:
        await bot.send_message(message.from_user.id, 'Введите сперва категорию и после сумму\n\nПример:  транспорт  150')
    except IndexError:
        await bot.send_message(message.from_user.id, 'Введите категорию и сумму через пробел\n\nПример:  транспорт  150')
