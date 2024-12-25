from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

api = '🤔'
bot = Bot(token=api)
dp = Dispatcher(bot, storage= MemoryStorage())

kb = ReplyKeyboardMarkup()
info = KeyboardButton(text='Информация')
calculate = KeyboardButton(text='Рассчитать')
kb.add(info)
kb.add(calculate)
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands='start')
async def start(message):
    print("Напечатан /start")
    await message.answer('Привет! Я бот помогающий твоему здороью.', reply_markup= kb)

@dp.message_handler(text = 'Рассчитать')
async def set_age(message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler()
async def all_massages(message):
    print(f'Напечатан {message.text}')
    await message.answer('Введите команду /start, чтобы начать общение.')

@dp.message_handler(text = 'Информация')
async def all_massages(message):
    print(f'Информация')
    await message.answer('🤔')


@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    data = await state.get_data()
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_growth(message, state):
    await state.update_data(growth = message.text)
    data = await state.get_data()
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    calories = 60 * int(data['weight']) + 6.25 * int(data['growth']) + 5 * int(data['age']) + 5
    await message.answer(f'Ваша норма калорий {calories}')
    await state.finish()
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)