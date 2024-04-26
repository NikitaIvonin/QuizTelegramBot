from ast import Index
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from aiogram.filters.command import Command
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from aiogram import F



from Data import update_quiz_index, get_quiz_index, get_player_result, create_table_qustions, create_table_results, update_player_results
from butt import generate_options_keyboard, get_question, quiz_data



# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Замените "YOUR_BOT_TOKEN" на токен, который вы получили от BotFather
API_TOKEN = '6533334543:AAFI_SgcEChC1FSeE2sKvuReSVLHB-YI9KE'


# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()



@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем сборщика клавиатур типа Reply
    builder = ReplyKeyboardBuilder()
    # Добавляем в сборщик одну кнопку
    builder.add(types.KeyboardButton(text="Начать игру"))
    # Прикрепляем кнопки к сообщению
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

async def new_quiz(message):
    # получаем id пользователя, отправившего сообщение
    user_id = message.from_user.id
    # сбрасываем значение текущего индекса вопроса квиза в 0
    current_question_index = 0
    current_result_index = 0
    await update_quiz_index(user_id, current_question_index)
    await update_player_results(user_id, current_result_index)

    # запрашиваем новый вопрос для квиза
    await get_question(message, user_id)

# Хэндлер на команды /quiz
@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    # Отправляем новое сообщение без кнопок
    await message.answer(f"Давайте начнем квиз!")
    # Запускаем новый квиз
    await new_quiz(message)



@dp.message(F.text=="Результат")
@dp.message(Command("result"))
async def player_result(message: types.Message):
    user_id = message.from_user.id
    current_result_index = await get_player_result(user_id)
    await message.answer(f"Ваш результат: %s "% current_result_index)


@dp.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Получение текущего вопроса для данного пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)

    #Получение результата для данного пользователя:
    current_result_index = await get_player_result(callback.from_user.id)

    correct_option = quiz_data[current_question_index]['correct_option']
    
    await callback.message.answer(f"Верно! Ваш ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    current_question_index += 1
    current_result_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)


    await update_player_results(callback.from_user.id, current_result_index)


    # Проверяем достигнут ли конец квиза
    if current_question_index < len(quiz_data):
        # Следующий вопрос
        await get_question(callback.message, callback.from_user.id)
    else:
        # Уведомление об окончании квиза
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        await callback.message.answer("Ваш результат: %s" % current_result_index)





@dp.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    # редактируем текущее сообщение с целью убрать кнопки (reply_markup=None)
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Получение текущего вопроса для данного пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)

    current_result_index = await get_player_result(callback.from_user.id)

    correct_option = quiz_data[current_question_index]['correct_option']

    # Отправляем в чат сообщение об ошибке с указанием верного ответа
    await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)


    await update_player_results(callback.from_user.id, current_result_index)


    # Проверяем достигнут ли конец квиза
    if current_question_index < len(quiz_data):
        # Следующий вопрос
        await get_question(callback.message, callback.from_user.id)
    else:
        # Уведомление об окончании квиза
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        await callback.message.answer("Ваш результат: %s" % current_result_index)

# Запуск процесса поллинга новых апдейтов
async def main():

    # Запускаем создание таблиц базы данных
    await create_table_qustions()
    await create_table_results()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())