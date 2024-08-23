from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions_2 import is_included, add_user, get_all_products


product_list = get_all_products()


api = '7040296994:AAFSywhWEgpoJdMVBj5NR_aT3B_6VEpCAlE'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb = ReplyKeyboardMarkup(resize_keyboard=True)
calc_button = KeyboardButton(text="Рассчитать")
info_button = KeyboardButton(text="Информация")
reg_button = KeyboardButton(text="Регистрация")
buy_button = KeyboardButton(text="Купить")
kb.row(calc_button, info_button)
kb.add(reg_button)
kb.add(buy_button)

inl_kb = InlineKeyboardMarkup()
inl_calc_button = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")
inl_form_button = InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")
inl_kb.row(inl_calc_button, inl_form_button)

gender_kb = InlineKeyboardMarkup()
male_button = InlineKeyboardButton(text="Муж.", callback_data="male")
female_button = InlineKeyboardButton(text="Жен.", callback_data="female")
gender_kb.row(male_button, female_button)

purchase_kb = InlineKeyboardMarkup()
for item in product_list:
    purchase_kb.add(InlineKeyboardButton(text=item[0], callback_data="product_buying"))


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=kb)


@dp.message_handler(text=['Регистрация'])
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await message.answer(f"Пользователь {message.text} существует, введите другое имя")
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age_db(message, state):
    await state.update_data(age=int(message.text))
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    if is_included(data['username']):
        await message.answer(f"Вы успешно зарегистрированы под ником {data['username']}", reply_markup=kb)
    else:
        await message.answer("Что-то пошло не так. Попробуйте повторить регистрацию чуть позже.", reply_markup=kb)
    await state.finish()


@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    for i, item_ in enumerate(product_list):
        await message.answer(f'Название: {item_[0]} | Описание: {item_[1]} | Цена: {item_[2]}')
        with open(f'product_imgs/prod_{i + 1}.webp', 'rb') as img:
            await message.answer_photo(img)

    await message.answer('Выберите продукт для покупки:', reply_markup=purchase_kb)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler(text=["Информация"])
async def get_info(message):
    await message.answer("Производится расчет оптимального числа калорий по формуле Миффлина-Сан Жеора")


@dp.message_handler(text=["Рассчитать"])
async def main_menu(message):
    await message.answer("Выбери опцию:", reply_markup=inl_kb)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("Муж.: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5\n"
                              + "Жен.: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161")
    await call.answer()


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст (полных лет):")
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост (см.):")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес (кг.):")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_gender(message, state):
    await state.update_data(weight=message.text)
    await message.answer("Ваш пол:", reply_markup=gender_kb)
    await UserState.gender.set()


@dp.callback_query_handler(state=UserState.gender, text="male")
async def send_calories_male(call, state):
    data = await state.get_data()
    result = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await call.message.answer(f"Оптимальное количество калорий: {result}", reply_markup=kb)
    await call.answer()
    await state.finish()


@dp.callback_query_handler(state=UserState.gender, text="female")
async def send_calories_female(call, state):
    data = await state.get_data()
    result = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
    await call.message.answer(f"Оптимальное количество калорий: {result}", reply_markup=kb)
    await call.answer()
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
