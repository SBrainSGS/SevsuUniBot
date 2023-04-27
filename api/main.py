import types
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

API_TOKEN = '5853267171:AAEvz3R_yfqmqVqZMkj0xkqORFGURfo4FO0'

# Инициализация бота, диспетчера и хранилища данных
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

# Команда '/start'
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):

    kb = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Я здесь первый раз, что расскажешь?',
        callback_data='first_time'
    ))
    kb.row(types.InlineKeyboardButton(
        text = 'Покажи мне все вопросы',
        callback_data='FAQ'
    ))

    await message.answer("Привет, абитуриент!\nМогу ли я что-то подсказать?", reply_markup=kb)

#Обработчики ответов
@dp.callback_query_handler(lambda call: call.data in ["FAQ"])
async def FAQ(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Посетить сайт',
        url='https://welcome.sevsu.ru/'
    ))
    kb.row(types.InlineKeyboardButton(
        text='Назад',
        callback_data='main'
    ))

    await call.message.edit_text("В <a href='https://telegra.ph/FAQ-04-25-11'>данном</a> разделе вы найдете все часто задаваемые вопросы. Если вы не нашли ответ на свой вопрос"
                                ", воспользуйтесь горячей линией университета или задайте вопрос в онлайн-чате на сайте.\n\n"
                                "Время работы контакт-центра: пн. - пт. с 09:00 до 17:00\n"
                                "Номер телефона: +7 (8692) 222-911\n"
                                "E-mail: priem@sevsu.ru", reply_markup=kb, parse_mode=ParseMode.HTML)

@dp.callback_query_handler(lambda call: call.data in ["first_time"])
async def first_time(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Да',
        callback_data='spec_yes'
    ))
    kb.row(types.InlineKeyboardButton(
        text='Нет',
        callback_data='spec_no'
    ))
    await call.message.edit_text("Хорошо, давай по порядку. Знаешь ли ты про наши специальности?", reply_markup=kb)


@dp.callback_query_handler(lambda call: call.data in ["spec_yes"])
async def spec_yes(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Да',
        callback_data='EGE_yes'
    ))
    kb.row(types.InlineKeyboardButton(
        text='Нет',
        callback_data='EGE_no'
    ))
    await call.message.edit_text('Теперь пройдемся по важной информации\nСдал ли ты ЕГЭ?', reply_markup=kb)

@dp.callback_query_handler(lambda call: call.data in ["spec_no"])
async def spec_no(call: types.CallbackQuery):
    wait = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Специальности',
        url='https://www.sevsu.ru/specialnosti/calculator/'
    ))
    wait.row(types.InlineKeyboardButton(
        text='Я вернулся',
        callback_data='spec_yes'
    ))

    await call.message.edit_text("Тогда держи ссылку, изучи внимательно\nКак разберешься, возвращайся ко мне", reply_markup=wait, parse_mode=ParseMode.HTML)

@dp.callback_query_handler(lambda call: call.data in ["EGE_yes"])
async def EGE_yes(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Давай проверим',
        callback_data='calc_yes'
    ))
    kb.row(types.InlineKeyboardButton(
        text='Нет, спасибо',
        callback_data='prog_no'
    ))

    await call.message.edit_text('Можешь воспользоваться калькулятором и проверить свои шансы на поступление',
                              reply_markup=kb)

@dp.callback_query_handler(lambda call: call.data in ["EGE_no"])
async def EGE_no(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Покажи',
        callback_data='prog_yes'
    ))
    kb.row(types.InlineKeyboardButton(
        text='Нет, спасибо',
        callback_data='prog_no'
    ))

    await call.message.edit_text('Можешь посмотреть программы подготовки', reply_markup=kb)


@dp.callback_query_handler(lambda call: call.data in ["calc_yes"])
async def calc_yes(call: types.CallbackQuery):
    wait = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Калькулятор ЕГЭ',
        url='https://www.sevsu.ru/specialnosti/calculator/'
    ))
    wait.row(types.InlineKeyboardButton(
        text='Я вернулся',
        callback_data='prog_no'
    ))

    await call.message.edit_text("Буду ждать тебя", reply_markup=wait)

@dp.callback_query_handler(lambda call: call.data in ["prog_yes"])
async def prog_yes(call: types.CallbackQuery):
    wait = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Программы подготовки',
        url = 'https://www.sevsu.ru/univers/kursy/pod-kursy/'
    ))
    wait.row(types.InlineKeyboardButton(
        text = 'Я вернулся',
        callback_data='prog_no'
    ))
    await call.message.edit_text("Внимательно читай!\nЖду тебя)", reply_markup=wait)

@dp.callback_query_handler(lambda call: call.data in ["prog_no"])
async def prog_no(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Да',
        callback_data='docs_yes'
    ))
    kb.row(types.InlineKeyboardButton(
        text='Нет',
        callback_data='docs_no'
    ))

    await call.message.edit_text('Тогда погнали дальше\nПодать документы ты сможешь лично в университете, через госуслуги'
                                ' (только для поступающих на высшее образование), в личном кабинете абитуриента и через почтовую связь\nРассказать о том как?', reply_markup=kb)


@dp.callback_query_handler(lambda call: call.data in ["docs_no"])
async def docs_no(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text = 'Конкурсные списки',
        url='https://www.sevsu.ru/uni/ekran/'
    ))
    kb.row(types.InlineKeyboardButton(
        text = 'Посетить сайт',
        url = 'https://welcome.sevsu.ru/'
    ))
    kb.row(types.InlineKeyboardButton(
        text='FAQ',
        callback_data='FAQ'
    ))
    kb.row(types.InlineKeyboardButton(
        text = 'Вернуться в начало',
        callback_data = 'main'
    ))

    await call.message.edit_text(
        "Двигаемся дальше\nВнимательно следи за конкурсными списками, чтобы узнать поступил ли ты\nВсю главную информацию я тебе рассказал. Если у тебя остались вопросы, то ты можешь посетить наш сайт"
        " или посмотреть часто задаваемые вопросы (FAQ)", reply_markup=kb, parse_mode=ParseMode.HTML)

@dp.callback_query_handler(lambda call: call.data in ["docs_yes"])
async def docs_yes(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Далее',
        callback_data='docs_no'
    ))

    await call.message.edit_text("<a href='https://telegra.ph/Kak-mozhno-podat-dokumenty-04-25-2'>Способы подачи документов</a>", reply_markup=kb, parse_mode=ParseMode.HTML)

@dp.callback_query_handler(lambda call: call.data in ["main"])
async def main(call: types.CallbackQuery, ):
    kb = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(
        text='Я здесь первый раз, что расскажешь?',
        callback_data='first_time'
    ))
    kb.row(types.InlineKeyboardButton(
        text = 'Покажи мне все вопросы',
        callback_data='FAQ'
    ))

    await call.message.edit_text("Привет, абитуриент!\nМогу ли я что-то подсказать?", reply_markup=kb)

if __name__ == '__main__':
   executor.start_polling(dp)