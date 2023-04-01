from aiogram import Bot, types
from aiogram.types import InlineKeyboardButton
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN
from models import DBManager


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = DBManager()

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(
        "Welcome!\n"\
        "I'm a bot where you can see online shop goods and Don't Forget to Join Telegram Channel : @DarkWebMarket_Store\n"\
        "To start write: /product"\
        )

@dp.message_handler(commands=['product'])
async def get_categories_command(msg: types.Message):
    """Getting all categories"""
    categories = db.get_categories()
    keyboard = types.InlineKeyboardMarkup()
    for category in categories:
        keyboard.add(
            InlineKeyboardButton(
                text=category,
                callback_data=f'ctg_{category}')
        )
    await bot.send_message(msg.from_user.id,'Categories:',reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data and call.data.startswith('ctg_'))
async def get_products_callback(callback_query: types.CallbackQuery):
    """Selects all products from a specific category"""
    query = callback_query.data.replace('ctg_','')# Убрать пометку callback'ов
    products = db.get_from_category(query)
    keyboard = types.InlineKeyboardMarkup()
    for product in products:
        keyboard.add(
            InlineKeyboardButton(
                text=product,
                callback_data=f'prdct_{product}'
            )
        )
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=f'{query}:',
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda call: call.data and call.data.startswith('prdct_'))
async def get_products_callback(callback_query: types.CallbackQuery):
    """Selects a product from a category"""
    query = callback_query.data.replace('prdct_','')# Убрать пометку callback'ов
    product = db.get_product(query)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text='Link',
            url=product[6]
        )
    )
    answer = f'*Product Name:*\n{product[1]}\n*Product description:*\n{product[2]}\n*Price:*{product[5]}'
    await bot.send_photo(
        chat_id=callback_query.from_user.id,
        caption=answer,
        reply_markup=keyboard,
        photo=product[3],
        parse_mode='markdown')

if __name__ == '__main__':
    executor.start_polling(dp)