from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
#from aiogram.methods.restrict_chat_member import RestrictChatMember
import asyncio
from seller import digiseller_api
from login import login
# import logging
# logging.basicConfig(filename='log.txt', filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S', level=logging.DEBUG)
# logging.info("Log started")

bot = Bot(token='')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    code = State()
    mail = State()
    password = State()
    pick_num = State()
    info = State()
    accept = State()


async def token():
    global token
    while True:
        token = digiseller_api().get_token()
        print(token)
        await asyncio.sleep(3600)


async def sales():
    while True:
        digiseller_api().get_sales(token)
        await asyncio.sleep(180)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Статус Товара 🗺').add('Товары Продавца 📦').add('Информация о Продавце 👔')
    # отправка начального сообщения после кнопки start
    await message.answer('Поздравляем, Вы находитесь в начале бота!🏠', reply_markup=keyboard)


@dp.message_handler(Text(equals='Статус Товара 🗺'))
async def check_id(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Отмена 🚫')
    await message.answer('Введите Ваш 16-значный уникальный код (без доп. символов и прочего) 📝', reply_markup=keyboard)
    #await bot(RestrictChatMember(message.from_user.id, ))
    await UserState.code.set()


@dp.message_handler(state=UserState.code)
async def process_message(message: types.Message, state: FSMContext):
    if message.text == 'Отмена 🚫' or message.text == '/start':
        await state.finish()
        return await start(message)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Отмена 🚫')
        await state.update_data(code=message.text)
        answer = digiseller_api().get_product_info(message.text, token)
        if answer == 'отсутствует или неверно задан параметр unique_code' or answer == 'не найден unique_code':
            return await message.answer(f'Введите уникальный код заново!🎛\n{answer}', reply_markup=keyboard)
        await message.reply(f'Ваш код был автоматически проверен системой!👍\n{answer}')
        await message.answer('Введите Ваш логин от Microsoft (Xbox) 🔒', reply_markup=keyboard)
        await UserState.next()


@dp.message_handler(state=UserState.mail)
async def process_message(message: types.Message, state: FSMContext):
    if message.text == 'Отмена 🚫' or message.text == '/start':
        await state.finish()
        return await start(message)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Отмена 🚫')
        await message.answer('Введите Ваш пароль от Microsoft (Xbox) 🔐', reply_markup=keyboard)
        await state.update_data(mail=message.text)
        await UserState.next()


@dp.message_handler(state=UserState.password)
async def process_message(message: types.Message, state: FSMContext):
    if message.text == 'Отмена 🚫' or message.text == '/start':
        await state.finish()
        return await start(message)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Отмена 🚫')
        await message.answer('Данные были получены, подождите несколько секунд 🔓')
        await state.update_data(password=message.text)
        data = await state.get_data()
        microsoft = login(data['mail'], data['password'])
        msg = microsoft.driver_start()
        if msg[0] == 'no_accept':
            await state.finish()
            with open('ENTERED.png', 'rb') as photo:
                await bot.send_photo(message.from_user.id, photo)
            await message.answer('Вход выполнен успешно!\nСпасибо за то, что воспользовались ботом!💛')
        elif msg[0] == 'accept':
            with open('ENTERED.png', 'rb') as photo:
                await bot.send_photo(message.from_user.id, photo)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Отмена')
            for i in range(1, msg[1] + 1):
                keyboard.add(str(i))
            await UserState.next()
            await message.answer('С помощью клавиатуры выберите один из удобных способов входа в аккаунт🎛', reply_markup=keyboard)
        elif msg[0] == 'screen_accept':
            with open('ENTERED.png', 'rb') as photo:
                await bot.send_photo(message.from_user.id, photo)
            await state.finish()
            await message.answer('Подтвердите вход, как сказано на скриншоте, после этого будет выполнен вход!⏳\nДальнейших сообщений вы не получите')
        else:
            await state.finish()
            return await message.answer(msg[0], reply_markup=keyboard)


@dp.message_handler(state=UserState.pick_num)
async def process_message(message: types.Message, state: FSMContext):
    if message.text == 'Отмена 🚫' or message.text == '/start':
        await state.finish()
        return await start(message)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Отмена 🚫')
        try:
            num = int(message.text)
        except ValueError:
            return await message.answer(f'Код может состоять только из цифр!🔢', reply_markup=keyboard)
        await message.answer('Секундочку', reply_markup=keyboard)
        await state.update_data(pick_num=num)
        data = await state.get_data()
        microsoft = login(data['mail'], data['password'])
        msg = microsoft.accept(num)
        await message.answer(msg[0], reply_markup=keyboard)
        if msg[1] == 1:
            await UserState.next()
        elif msg[1] == 2:
            await UserState.next()
        elif msg[1] == 3:
            await state.finish()
            await message.answer("Подтвердите вход в приложении, на этом бот с Вами прощается 💛")


@dp.message_handler(state=UserState.info)
async def process_message(message: types.Message, state: FSMContext):
    if message.text == 'Отмена 🚫' or message.text == '/start':
        await state.finish()
        return await start(message)
    else:
        await state.update_data(info=message.text)
        data = await state.get_data()
        microsoft = login(data['mail'], data['password'])
        microsoft.accept_1(data['pick_num'], message.text)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Отмена 🚫')
        await message.answer('Введите отправленный Вам код✏', reply_markup=keyboard)
        await UserState.next()


@dp.message_handler(state=UserState.accept)
async def process_message(message: types.Message, state: FSMContext):
    if message.text == 'Отмена 🚫' or message.text == '/start':
        await state.finish()
        return await start(message)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Отмена 🚫')
        await message.answer('Заходим⏳', reply_markup=keyboard)
        await state.update_data(accept=message.text)
        data = await state.get_data()
        microsoft = login(data['mail'], data['password'])
        msg = microsoft.accept_2(data['pick_num'], message.text)
        await state.finish()
        with open('ENTERED.png', 'rb') as photo:
            await bot.send_photo(message.from_user.id, photo)
        await message.answer('Вход выполнен успешно!\nСпасибо за то, что воспользовались ботом!💛')


@dp.message_handler(Text(equals='Информация о Продавце 👔'))
async def info_seller(message: types.Message):
    await message.answer('✅Контактные данные для связи и вопросов:\nTelegram: https://t.me/PipSqick\nDiscord: SkyshadoW#7050\nVK: https://vk.com/pipsqick\nПочта: skyshadow.sky@inbox.ru')


@dp.message_handler(Text(equals='Товары Продавца 📦'))
async def info_products(message: types.Message):
    await message.answer('📦 Все товары продавца вы сможете найти на данной странице: https://plati.market/seller/sky-shop/1078014/',
                         disable_web_page_preview=True)


@dp.message_handler(Text(equals='Отмена 🚫'))
async def info_seller(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Статус Товара 🗺').add('Товары Продавца 📦').add('Информация о Продавце 👔')
    await message.answer('Вы вернулись в начало бота🏠', reply_markup=keyboard)


if __name__ == '__main__':
    asyncio.get_event_loop().create_task(token())
    asyncio.get_event_loop().create_task(sales())
    executor.start_polling(dp, skip_updates=True)

