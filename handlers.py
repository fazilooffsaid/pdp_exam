from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
import db

user_lang = {}

lang_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇺🇿 O'zbek"), KeyboardButton(text="🇬🇧 English")]
    ],
    resize_keyboard=True
)

def main_kb(lang):
    if lang == "uz":
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🍽 Restoran menyusi")],
                [KeyboardButton(text="📞 Bog'lanish")]
            ],
            resize_keyboard=True
        )
    else:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🍽 Restaurant menu")],
                [KeyboardButton(text="📞 Contact")]
            ],
            resize_keyboard=True
        )


def menu_kb(lang):
    if lang == "uz":
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🥗 Salatlar")],
                [KeyboardButton(text="🍔 Fast Food")],
                [KeyboardButton(text="🍲 Issiq taomlar")],
                [KeyboardButton(text="⬅️ Orqaga")]
            ],
            resize_keyboard=True
        )
    else:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🥗 Salads")],
                [KeyboardButton(text="🍔 Fast Food")],
                [KeyboardButton(text="🍲 Hot meals")],
                [KeyboardButton(text="⬅️ Back")]
            ],
            resize_keyboard=True
        )


def make_kb(items, back_text):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=i)] for i in items] + [[KeyboardButton(text=back_text)]],
        resize_keyboard=True
    )


async def start(message: Message):
    await message.answer("Tilni tanlang / Choose language", reply_markup=lang_kb)


async def handle_message(message: Message):
    user_id = message.from_user.id
    text = message.text

    if text == "🇺🇿 O'zbek":
        user_lang[user_id] = "uz"
        await message.answer("Asosiy menyu:", reply_markup=main_kb("uz"))
        return

    if text == "🇬🇧 English":
        user_lang[user_id] = "en"
        await message.answer("Main menu:", reply_markup=main_kb("en"))
        return

    lang = user_lang.get(user_id)

    if not lang:
        await message.answer("Tilni tanlang / Choose language", reply_markup=lang_kb)
        return

    if lang == "uz":

        if text == "🍽 Restoran menyusi":
            await message.answer("Menyuni tanlang:", reply_markup=menu_kb("uz"))

        elif text == "📞 Bog'lanish":
            await message.answer("📱 Aloqa: +998 90 000 00 00")

        elif text == "🥗 Salatlar":
            foods = db.get_foods_by_category("salads")
            await message.answer("Salatlar:", reply_markup=make_kb(foods, "⬅️ Orqaga"))

        elif text == "🍔 Fast Food":
            foods = db.get_foods_by_category("fastfood")
            await message.answer("Fast food:", reply_markup=make_kb(foods, "⬅️ Orqaga"))

        elif text == "🍲 Issiq taomlar":
            foods = db.get_foods_by_category("hot")
            await message.answer("Issiq taomlar:", reply_markup=make_kb(foods, "⬅️ Orqaga"))

        elif text == "⬅️ Orqaga":
            await message.answer("Asosiy menyu:", reply_markup=main_kb("uz"))

    else:

        if text == "🍽 Restaurant menu":
            await message.answer("Choose menu:", reply_markup=menu_kb("en"))

        elif text == "📞 Contact":
            await message.answer("📱 Phone: +998 90 000 00 00")

        elif text == "🥗 Salads":
            foods = db.get_foods_by_category("salads")
            await message.answer("Salads:", reply_markup=make_kb(foods, "⬅️ Back"))

        elif text == "🍔 Fast Food":
            foods = db.get_foods_by_category("fastfood")
            await message.answer("Fast food:", reply_markup=make_kb(foods, "⬅️ Back"))

        elif text == "🍲 Hot meals":
            foods = db.get_foods_by_category("hot")
            await message.answer("Hot meals:", reply_markup=make_kb(foods, "⬅️ Back"))

        elif text == "⬅️ Back":
            await message.answer("Main menu:", reply_markup=main_kb("en"))