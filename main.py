import types
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode

API_TOKEN = '5853267171:AAEvz3R_yfqmqVqZMkj0xkqORFGURfo4FO0'

# Инициализация бота, диспетчера и хранилища данных
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


# Форма ожидания ввода данных
class Form(StatesGroup):
    name = State()


# Команда '/start'
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Привет, абитуриент! Перед началом работы тебе следует пройти регистрацию")
    await message.answer("Введите ФИО полностью:")
    await Form.name.set()


# Команда отмены ожидания ввода
@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Cancelled.')


# Ожидание ввода ФИО
@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    kb = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Я здесь первый раз, что расскажешь?',
        callback_data='first_time'
    ))
    kb.row(types.InlineKeyboardButton(
        text = 'Покажи мне все вопросы',
        callback_data='menu'
    ))

    await state.finish()
    await message.answer("Регистрация прошла успешно")


    await message.answer("Могу ли я что-то подсказать?", reply_markup=kb)


# Обработчики ответов
@dp.callback_query_handler(text='main')
async def main(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Я здесь первый раз, что расскажешь?',
        callback_data='first_time'
    ))
    kb.row(types.InlineKeyboardButton(
        text='Да, хочу уточнить пару вопросов',
        callback_data='FAQ'
    ))

    await call.message.answer("Могу ли я что-то подсказать?", reply_markup=kb)



@dp.callback_query_handler(text='FAQ')
async def FAQ(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text = 'FAQ',
        url = 'https://www.sevsu.ru/admission/faq/'
    ))
    kb.row(types.InlineKeyboardButton(
        text = 'Назад',
        callback_data = 'main'
    ))

    await call.message.answer('В разделе FAQ вы найдете все часто задаваемые вопросы. Если вы не нашли ответ на свой вопрос'
                              ', воспользуйтесь горячей линией университета или задайте вопрос в онлайн-чате на сайте.\n\n'
                              'Время работы контакт-центра: пн. - пт. с 09:00 до 17:00\n'
                              'Номер телефона: +7 (8692) 222-911\n'
                              'E-mail: priem@sevsu.ru', reply_markup=kb)

@dp.callback_query_handler(text='first_time')
async def first_time(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Да',
        callback_data='spec_yes'
    ))
    kb.row(types.InlineKeyboardButton(
        text='Нет',
        callback_data='spec_no'
    ))

    await call.message.answer("Хорошо, давай по порядку")
    await call.message.answer("Знаешь ли ты про наши специальности?", reply_markup=kb)


@dp.callback_query_handler(text='spec_yes')
async def spec_yes(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Да',
        callback_data='EGE_yes'
    ))
    kb.row(types.InlineKeyboardButton(
        text='Нет',
        callback_data='EGE_no'
    ))

    await call.message.answer('Тогда к следующему пункту')

    await call.message.answer('Теперь пройдемся по важной информации')
    await call.message.answer('Прочитай правила приёма, пригодится!')
    await call.message.answer("<a href='https://www.sevsu.ru/admission/item/85-pravila-priema/'>Правила приёма</a>",
                              parse_mode=ParseMode.HTML)

    await call.message.answer('Сдал ли ты ЕГЭ?', reply_markup=kb)


@dp.callback_query_handler(text='spec_no')
async def spec_no(call: types.CallbackQuery):
    wait = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Я вернулся',
        callback_data='spec_yes'
    ))

    await call.message.answer('Тогда держи ссылку, изучи внимательно')
    await call.message.answer("<a href='https://www.sevsu.ru/specialnosti/'>Специальности</a>",
                              parse_mode=ParseMode.HTML)
    await call.message.answer('Как разберешься, возвращайся ко мне', reply_markup=wait)


@dp.callback_query_handler(text='EGE_yes')
async def EGE_yes(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Давай проверим',
        callback_data='calc_yes'
    ))
    kb.row(types.InlineKeyboardButton(
        text='Нет, спасибо',
        callback_data='calc_no'
    ))

    await call.message.answer('Можешь воспользоваться калькулятором и проверить свои шансы на поступление',
                              reply_markup=kb)


@dp.callback_query_handler(text='EGE_no')
async def EGE_no(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Покажи',
        callback_data='prog_yes'
    ))
    kb.row(types.InlineKeyboardButton(
        text='Нет, спасибо',
        callback_data='calc_no'
    ))

    await call.message.answer('Можешь посмотреть программы подготовки', reply_markup=kb)


@dp.callback_query_handler(text='calc_yes')
async def calc_yes(call: types.CallbackQuery):
    wait = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Я вернулся',
        callback_data='calc_no'
    ))

    await call.message.answer("<a href='https://www.sevsu.ru/specialnosti/calculator/'>Калькулятор ЕГЭ</a>",
                              parse_mode=ParseMode.HTML)
    await call.message.answer('Буду ждать тебя', reply_markup=wait)


@dp.callback_query_handler(text='prog_yes')
async def prog_yes(call: types.CallbackQuery):
    wait = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Я вернулся',
        callback_data='calc_no'
    ))

    await call.message.answer("<a href='https://www.sevsu.ru/univers/kursy/pod-kursy/'>Программы подготовки</a>",
                              parse_mode=ParseMode.HTML)
    await call.message.answer('Жду тебя)', reply_markup=wait)


@dp.callback_query_handler(text='calc_no')
async def prog_no(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Да',
        callback_data='docs_yes'
    ))
    kb.row(types.InlineKeyboardButton(
        text='Нет',
        callback_data='docs_no'
    ))

    await call.message.answer('Тогда погнали дальше')
    await call.message.answer('Подать документы ты сможешь лично в университете, через госуслуги'
                              ' (только для поступающих на высшее образование), в личном кабинете аббитуриента и через почтовую связь')
    await call.message.answer('Рассказать о том как?', reply_markup=kb)


@dp.callback_query_handler(text='docs_no')
async def docs_no(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Посетить сайт',
        url='https://welcome.sevsu.ru/'
    ))
    kb.row(types.InlineKeyboardButton(
        text='FAQ',
        callback_data='FAQ'
    ))

    await call.message.answer('Двигаемся дальше')
    await call.message.answer('Внимательно следи за конкурсными списками, чтобы узнать поступил ли ты')
    await call.message.answer("<a href='https://www.sevsu.ru/uni/ekran/'>Конкурсные списки</a>",
                              parse_mode=ParseMode.HTML)
    await call.message.answer(
        'Всю главную информацию я тебе рассказал. Если у тебя остались вопросы, то ты можешь посетить наш сайт'
        ' или посмотреть часто задаваемые вопросы (FAQ)', reply_markup=kb)


@dp.callback_query_handler(text='docs_yes')
async def docs_yes(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Лично в университете',
        url='https://www.sevsu.ru/admission/item/9539-ochno/'
    ))
    kb.row(types.InlineKeyboardButton(
        text='Через Госуслуги(только для поступающих на высшее образование)',
        url='https://www.sevsu.ru/admission/item/9397-gosuslugi/'
    ))
    kb.row(types.InlineKeyboardButton(
        text='Через личный кабинет абитуриента',
        url='https://www.sevsu.ru/admission/item/9398-lk/'
    ))
    kb.row(types.InlineKeyboardButton(
        text='Через почтовую связь',
        url='https://www.sevsu.ru/admission/item/9540-oper/'
    ))
    kb.row(types.InlineKeyboardButton(
        text='Далее',
        callback_data='docs_no'
    ))

    await call.message.answer('Выбери метод подачи документов', reply_markup=kb)

if __name__ == '__main__':
   executor.start_polling(dp)