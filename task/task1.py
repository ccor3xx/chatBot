
from aiogram import Router, types, F, Bot
from aiogram.types import LabeledPrice, PreCheckoutQuery, FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from Main.Config import TOKEN_YOUCASSA, table_link
from gspread import Client, Spreadsheet, Worksheet, service_account, exceptions

router = Router()
#Создаю клавиатуру для выполнения заданий.
async def reply_kbd()-> types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text='Ленина, 1'))
    builder.row(types.KeyboardButton(text='Оплата 2 р.'))
    builder.row(types.KeyboardButton(text='Изображение'))
    builder.row(types.KeyboardButton(text='Значение из таблицы'))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)



#ответ на нажатие кнопки Ленина, 1.
@router.message(F.text.lower() == 'ленина, 1')
async def send_dot_on_map(message: types.Message):
    url = 'https://yandex.ru/maps/-/CDGdIC4s'
    keyboard = await reply_kbd()
    await message.answer(f'Ссылка на точку на карте: {url}', reply_markup=keyboard)

#Подключаю ЮКасса.Тест для совершения оплаты.
@router.message(F.text.lower() == 'оплата 2 р.')
async def send_payment(message: types.Message):
    keyboard = await reply_kbd()
    await message.answer_invoice(title='Оплата 2 р',
                                 description='Оплата 2 р',
                                 provider_token=TOKEN_YOUCASSA,
                                 payload='send_payment',
                                 currency='RUB',
                                 prices=[LabeledPrice(label='Оплата 2р.', amount=9200)], #минимальная сумма оплаты для API телеграм 91,35
                                 start_parameter='unique_parameter_' + str(message.from_user.id),
                                 reply_markup=None)
#Обработчик успешной оплаты.
async def pre_checkout(message: types.Message, query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(query.id, ok=True)
    await message.answer(text='Оплата успешно отправлена')

#Ответ на нажате кнопки отправки изображения.
@router.message(F.text.lower() == 'изображение')
async def send_image(message: types.Message):
    photo = FSInputFile(path = r'P:\Coded\ChatBot\photo.jpg', filename='photo.jpg')
    await message.answer_photo(photo=photo, caption='Прекрасный пейзаж')

#Ответ на нажатие кнопки получения значения из таблицы.
gc: Client = service_account(r'P:\Coded\ChatBot\google_sheets_api.json')
sh: Spreadsheet = gc.open_by_url(table_link)
@router.message(F.text.lower() == 'значение из таблицы')
async def send_table(message: types.Message):
    ws = sh.sheet1
    val = ws.acell('A2').value
    await message.answer(f'Значение из таблицы для ячейки А2: {val}')

