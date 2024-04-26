from aiogram.filters.command import Command
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import Bot, Dispatcher, types
from Data import update_quiz_index, get_quiz_index

dp = Dispatcher()

quiz_data = [
    {
        'question': 'Что такое Python?',
        'options': ['Язык программирования', 'Тип данных', 'Музыкальный инструмент', 'Змея на английском'],
        'correct_option': 0
    },
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': ['int', 'float', 'str', 'natural'],
        'correct_option': 0
    },
    {
        'question': 'Как правильно комментировать одну строку в Python?',
        'options': ['# Это комментарий', '// Это комментарий', '/* Это комментарий */', '<!-- Это комментарий -->'],
        'correct_option': 0
    },
    {
        'question': "В Python, какова цель оператора 'if'?",
        'options': ['Определение функции', 'Выполнение кода в зависимости от условия', 'Создание цикла', 'Вывод текста на консоль'],
        'correct_option': 1
    },
    {
        'question': "Для чего в Python используется ключевое слово 'None'?",
        'options': ['Для определения булевой переменной', 'Для создания цикла', 'Для представления отсутствия значения или нулевого значения', 'Для вывода текста на консоль'],
        'correct_option': 2
    },
    {
        'question': "Для чего в Python используются блоки 'try' и 'except'?",
        'options': ['Для создания цикла', 'Для определения функции', 'Для обработки исключений или ошибок в коде', 'Для вывода текста на консоль'],
        'correct_option': 2
    },
    {
        'question': "Какой результат выдаст 'list(range(5))' в Python?",
        'options': ['[0, 1, 2, 3, 4]', '[1, 2, 3, 4, 5]', '[5, 4, 3, 2, 1, 0]', 'Ошибка'],
        'correct_option': 0
    },
    {
        'question': "Что делает 'str(123)' в Python?",
        'options': ["Ничего не делает, так как '123' уже является строкой", "Преобразует строку '123' в число 123", 'Генерирует ошибку', "Преобразует число 123 в строку '123'"],
        'correct_option': 3
    },
    {
        'question': "Для чего обычно используется 'asyncio' в Python?",
        'options': ['Для написания параллельного кода с использованием синтаксиса async/await', 'Для выполнения фоновой обработки', 'Для красоты', 'Для управления асинхронными сетевыми соединениями'],
        'correct_option': 0
    },
    {
        'question': "Для чего в основном используется 'scikit-learn' в Python?",
        'options': ['Для построения ООП', 'Для веб-разработки', 'Для системного скриптинга', 'Для машинного обучения'],
        'correct_option': 3
    }
]

async def get_question(message, user_id):

    # Запрашиваем из базы текущий индекс для вопроса
    current_question_index = await get_quiz_index(user_id)
    # Получаем индекс правильного ответа для текущего вопроса
    correct_index = quiz_data[current_question_index]['correct_option']
    # Получаем список вариантов ответа для текущего вопроса
    opts = quiz_data[current_question_index]['options']

    # Функция генерации кнопок для текущего вопроса квиза
    # В качестве аргументов передаем варианты ответов и значение правильного ответа (не индекс!)
    kb = generate_options_keyboard(opts, opts[correct_index])
    # Отправляем в чат сообщение с вопросом, прикрепляем сгенерированные кнопки
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

def generate_options_keyboard(answer_options, right_answer):
  # Создаем сборщика клавиатур типа Inline
    builder = InlineKeyboardBuilder()

    # В цикле создаем 4 Inline кнопки, а точнее Callback-кнопки
    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            # Текст на кнопках соответствует вариантам ответов
            text=option,
            # Присваиваем данные для колбэк запроса.
            # Если ответ верный сформируется колбэк-запрос с данными 'right_answer'
            # Если ответ неверный сформируется колбэк-запрос с данными 'wrong_answer'
            callback_data="right_answer" if option == right_answer else "wrong_answer")
        )

    # Выводим по одной кнопке в столбик
    builder.adjust(1)
    return builder.as_markup()